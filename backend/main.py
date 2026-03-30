import os
import json
import shutil
import pathlib
from datetime import datetime
from typing import List, Optional

import bcrypt
from fastapi import FastAPI, Depends, HTTPException, File, UploadFile, Form, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from . import models, schemas
from .database import engine, get_db
from .services.ai_screening import calculate_fit_score

# ─── GOOGLE CLIENT ID ─────────────────────────────────────────────────────────
GOOGLE_CLIENT_ID = os.getenv(
    "GOOGLE_CLIENT_ID",
    "21454828522-imfo3lhi3hrg4846hpm0m7fbn69t6ds0.apps.googleusercontent.com"
)

# ─── PASSWORD HELPERS ─────────────────────────────────────────────────────────
def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))

# ─── DB INIT ──────────────────────────────────────────────────────────────────
models.Base.metadata.create_all(bind=engine)

# ─── APP ──────────────────────────────────────────────────────────────────────
app = FastAPI(title="Nukhba Elite API | Talent Intelligence")

# CORS — allow all origins for API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── STATIC FRONTEND ──────────────────────────────────────────────────────────
_STATIC = pathlib.Path(__file__).parent.parent / "frontend" / "web"
app.mount("/web", StaticFiles(directory=str(_STATIC), html=True), name="web")

@app.get("/", include_in_schema=False)
def root_redirect():
    return RedirectResponse(url="/web/index.html")

# ─── STARTUP SEED ─────────────────────────────────────────────────────────────
@app.on_event("startup")
def startup_event():
    from .database import SessionLocal
    db = SessionLocal()
    try:
        _seed_database(db)
    except Exception as e:
        print(f"[WARNING] Seed skipped (non-fatal): {e}")
    finally:
        db.close()

# ─── CONFIG ENDPOINT ──────────────────────────────────────────────────────────
@app.get("/config")
def get_config():
    """Frontend fetches this to get the Google Client ID dynamically."""
    client_id = GOOGLE_CLIENT_ID if GOOGLE_CLIENT_ID not in ("", "YOUR_GOOGLE_CLIENT_ID_HERE") else None
    return {"google_client_id": client_id}

# ─── GOOGLE SIGN-IN VERIFY ────────────────────────────────────────────────────
@app.post("/users/google-verify", response_model=schemas.UserResponse)
def google_verify(data: schemas.GoogleVerifyToken, db: Session = Depends(get_db)):
    """
    Verifies a Google Identity Services credential JWT.
    Creates or finds the user in the database.
    """
    try:
        from google.oauth2 import id_token
        from google.auth.transport import requests as google_requests
        idinfo = id_token.verify_oauth2_token(
            data.credential,
            google_requests.Request(),
            GOOGLE_CLIENT_ID,
        )
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid Google token: {str(e)}")

    google_id  = idinfo["sub"]
    email      = idinfo.get("email", "")
    name       = idinfo.get("name", "Unknown")
    avatar_url = idinfo.get("picture", "")

    # Try find by Google ID first (returning user)
    user = db.query(models.User).filter(models.User.google_id == google_id).first()
    if not user:
        # Try link to existing email account
        user = db.query(models.User).filter(models.User.email == email).first()
        if user:
            user.google_id    = google_id
            user.avatar_url   = avatar_url
            user.auth_provider = "google"
            db.commit()
            db.refresh(user)
        else:
            # Brand-new user
            user = models.User(
                name=name,
                email=email,
                google_id=google_id,
                avatar_url=avatar_url,
                auth_provider="google",
                role=data.role or "Candidate",
                password=None,
            )
            db.add(user)
            db.commit()
            db.refresh(user)

    return user

# ─── LEGACY GOOGLE-AUTH ENDPOINT (kept for compatibility) ─────────────────────
@app.post("/users/google-auth", response_model=schemas.UserResponse)
def google_auth(data: schemas.GoogleAuthCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.google_id == data.google_id).first()
    if not user:
        user = db.query(models.User).filter(models.User.email == data.email).first()
        if user:
            user.google_id    = data.google_id
            user.avatar_url   = data.avatar_url
            user.auth_provider = "google"
            db.commit(); db.refresh(user)
        else:
            user = models.User(
                name=data.name, email=data.email,
                google_id=data.google_id, avatar_url=data.avatar_url,
                auth_provider="google", role=data.role or "Candidate", password=None,
            )
            db.add(user); db.commit(); db.refresh(user)
    return user

# ─── USER ENDPOINTS ───────────────────────────────────────────────────────────
@app.post("/users/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if not user.email or not user.password:
        raise HTTPException(status_code=400, detail="Email and password are required")
    if len(user.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")

    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = get_password_hash(user.password)
    new_user = models.User(
        name=user.name, email=user.email, password=hashed,
        role=user.role, phone=user.phone, country=user.country,
    )
    db.add(new_user); db.commit(); db.refresh(new_user)

    # Persistent JSON backup
    _append_json("backend/data/users_backup.json", {
        "name": user.name, "email": user.email, "role": user.role,
        "phone": user.phone, "country": user.country, "timestamp": str(datetime.now()),
    })
    return new_user

@app.post("/users/login", response_model=schemas.UserResponse)
def login_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()

    if not db_user:
        _append_json("backend/data/login_logs.json", {
            "email": user.email, "timestamp": str(datetime.now()), "status": "Failed - not found"
        })
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # Google-only account
    if db_user.auth_provider == "google" and not db_user.password:
        raise HTTPException(
            status_code=400,
            detail="This account uses Google Sign-In. Please use the 'Continue with Google' button."
        )

    if not db_user.password or not verify_password(user.password or "", db_user.password):
        _append_json("backend/data/login_logs.json", {
            "email": user.email, "timestamp": str(datetime.now()), "status": "Failed - wrong password"
        })
        raise HTTPException(status_code=400, detail="Invalid credentials")

    _append_json("backend/data/login_logs.json", {
        "email": user.email, "timestamp": str(datetime.now()), "status": "Success"
    })
    return db_user

@app.put("/users/reset-password")
def reset_password(data: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == data.email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if not data.password:
        raise HTTPException(status_code=400, detail="New password required")
    db_user.password = get_password_hash(data.password)
    db.commit()
    return {"message": "Password reset successfully"}

@app.post("/users/{user_id}/profile", response_model=schemas.UserResponse)
async def update_profile(
    user_id: int, 
    auto_apply: bool = Form(...),
    resume_text: Optional[str] = Form(None),
    resume_file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    extracted_text = None
    if resume_file and resume_file.filename:
        try:
            import fitz # PyMuPDF
            content = await resume_file.read()
            doc = fitz.open(stream=content, filetype="pdf")
            extracted_text = ""
            for page in doc:
                extracted_text += page.get_text()
            extracted_text = extracted_text.strip()
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to extract PDF text: {str(e)}")
            
    final_text = extracted_text or resume_text or user.resume_text
    
    user.auto_apply = auto_apply
    user.resume_text = final_text
    db.commit()
    db.refresh(user)
    return user

# ─── JOB ENDPOINTS ────────────────────────────────────────────────────────────
def perform_auto_apply(job_id: int):
    from .database import SessionLocal
    db = SessionLocal()
    try:
        job = db.query(models.Job).filter(models.Job.id == job_id).first()
        if not job: return
        
        candidates = db.query(models.User).filter(
            models.User.role == "Candidate", 
            models.User.auto_apply == True,
            models.User.resume_text != None
        ).all()
        
        for candidate in candidates:
            existing = db.query(models.Application).filter(
                models.Application.job_id == job.id,
                models.Application.candidate_id == candidate.id
            ).first()
            if existing: continue
            
            ai_result = calculate_fit_score(candidate.resume_text, job.requirements)
            new_app = models.Application(
                job_id=job.id,
                candidate_id=candidate.id,
                resume_text=candidate.resume_text,
                ai_score=ai_result["score"],
                ai_feedback=ai_result["feedback"],
                status="Screened",
            )
            db.add(new_app)
        db.commit()
    except Exception as e:
        print(f"[AUTO-APPLY ERROR]: {e}")
    finally:
        db.close()

@app.post("/jobs", response_model=schemas.JobResponse)
def create_job(job: schemas.JobCreate, hr_id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    new_job = models.Job(**job.dict(), hr_id=hr_id, status="Open")
    db.add(new_job); db.commit(); db.refresh(new_job)
    
    background_tasks.add_task(perform_auto_apply, new_job.id)
    return new_job

@app.get("/jobs", response_model=List[schemas.JobResponse])
def get_jobs(db: Session = Depends(get_db)):
    return db.query(models.Job).all()

# ─── APPLICATION ENDPOINTS ────────────────────────────────────────────────────
@app.post("/applications", response_model=schemas.ApplicationResponse)
async def apply_job(
    candidate_id: int, 
    job_id: int = Form(...),
    resume_text: Optional[str] = Form(None),
    resume_file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    existing = db.query(models.Application).filter(
        models.Application.job_id == job_id,
        models.Application.candidate_id == candidate_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already applied to this job")

    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    extracted_text = ""
    if resume_file and resume_file.filename:
        try:
            import fitz
            content = await resume_file.read()
            doc = fitz.open(stream=content, filetype="pdf")
            for page in doc:
                extracted_text += page.get_text()
            extracted_text = extracted_text.strip()
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to extract PDF text: {str(e)}")
            
    final_resume_text = extracted_text or resume_text or ""
    if not final_resume_text.strip():
        raise HTTPException(status_code=400, detail="A resume (PDF or text) is required.")

    ai_result = calculate_fit_score(final_resume_text, job.requirements)
    score = ai_result["score"]
    
    # ─── AUTO-ROUTING & STORAGE CONTROL ───
    if score is not None and score < 50.0:
        status = "Rejected"
        db_resume_text = "Discarded to save storage (Unmatched Candidate)"
    elif score is not None and score >= 75.0:
        status = "Shortlisted"
        db_resume_text = final_resume_text
    else:
        status = "Screened"
        db_resume_text = final_resume_text

    new_app = models.Application(
        job_id=job_id,
        candidate_id=candidate_id,
        resume_text=db_resume_text,
        ai_score=score,
        ai_feedback=ai_result["feedback"],
        status=status,
    )
    db.add(new_app); db.commit(); db.refresh(new_app)

    # Save physical file ONLY if matched to save disk space
    if score is not None and score >= 50.0:
        os.makedirs("backend/data/resumes", exist_ok=True)
        fname = f"backend/data/resumes/app_{new_app.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(fname, "w", encoding="utf-8") as f:
            f.write(f"Candidate: {candidate_id}\nJob: {new_app.job_id}\nScore: {new_app.ai_score}\n\n{final_resume_text}")

    return new_app

@app.get("/applications/{job_id}", response_model=List[schemas.ApplicationResponse])
def get_applications_for_job(job_id: int, db: Session = Depends(get_db)):
    return db.query(models.Application).filter(
        models.Application.job_id == job_id,
        models.Application.status != "Rejected"  # Auto-hide discards
    ).all()

@app.get("/applications/candidate/{candidate_id}", response_model=List[schemas.ApplicationResponse])
def get_candidate_applications(candidate_id: int, db: Session = Depends(get_db)):
    return db.query(models.Application).filter(models.Application.candidate_id == candidate_id).all()

@app.put("/applications/{app_id}/status")
def update_application_status(app_id: int, status: str, db: Session = Depends(get_db)):
    application = db.query(models.Application).filter(models.Application.id == app_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    application.status = status
    db.commit()
    return {"message": "Status updated successfully"}

# ─── SYSTEM ENDPOINTS ─────────────────────────────────────────────────────────
@app.post("/system/seed")
def seed_database(db: Session = Depends(get_db)):
    return _seed_database(db)

@app.get("/system/download-data")
def download_data():
    zip_path = "system_backup"
    shutil.make_archive(zip_path, "zip", "backend/data")
    return FileResponse(
        path=f"{zip_path}.zip",
        filename=f"Nukhba_Backup_{datetime.now().strftime('%Y%m%d')}.zip",
        media_type="application/zip",
    )

# ─── INTERNAL HELPERS ─────────────────────────────────────────────────────────
def _append_json(path: str, record: dict):
    """Safely appends a record to a JSON array file."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    data = []
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                data = json.load(f)
        except Exception:
            data = []
    data.append(record)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def _seed_database(db: Session):
    """Seeds demo users and jobs. Safe to call multiple times."""
    # HR user
    if not db.query(models.User).filter(models.User.email == "hr@example.com").first():
        db.add(models.User(
            name="HR Manager", email="hr@example.com",
            password=get_password_hash("password123"), role="HR",
            country="United Arab Emirates 🇦🇪", phone="+971 50 123 4567",
        ))
        db.commit()

    # Candidate user
    if not db.query(models.User).filter(models.User.email == "candidate@example.com").first():
        db.add(models.User(
            name="John Doe", email="candidate@example.com",
            password=get_password_hash("password123"), role="Candidate",
            country="United Arab Emirates 🇦🇪", phone="+971 50 765 4321",
        ))
        db.commit()

    # Sample jobs
    hr = db.query(models.User).filter(models.User.email == "hr@example.com").first()
    sample_jobs = [
        {"title": "Senior Software Engineer",
         "description": "We are looking for a backend pro to join our fintech scaling team.",
         "requirements": "Python, FastAPI, SQLAlchemy, PostgreSQL, Docker, AWS"},
        {"title": "Product Designer",
         "description": "Design the future of AI interfaces with our creative team.",
         "requirements": "Figma, UI/UX, Design Systems, Prototyping, Adobe Creative Suite"},
        {"title": "Data Scientist",
         "description": "Leverage LLMs and data to build smart recruitment features.",
         "requirements": "Python, PyTorch, Transformers, NLP, Statistics, Pandas"},
    ]
    for j in sample_jobs:
        if not db.query(models.Job).filter(models.Job.title == j["title"]).first():
            db.add(models.Job(**j, hr_id=hr.id, status="Open"))
    db.commit()

    return {"message": "Database seeded successfully"}
