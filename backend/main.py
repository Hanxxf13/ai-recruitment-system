from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import json
import shutil
from datetime import datetime

from . import models
from . import schemas
from .database import engine, get_db
from .services.ai_screening import calculate_fit_score
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Nukhba Elite API | Talent Intelligence")

@app.get("/", include_in_schema=False)
def root_redirect():
    return RedirectResponse(url="/docs")

# Auto-seed on startup for Render ephemeral storage
@app.on_event("startup")
def startup_event():
    from .database import SessionLocal
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- USER ENDPOINTS ---
@app.post("/users/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = models.User(
        name=user.name, email=user.email, password=user.password, role=user.role,
        phone=user.phone, country=user.country
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    # Persistent Backup (JSON)
    backup_path = "backend/data/users_backup.json"
    users_data = []
    if os.path.exists(backup_path):
        with open(backup_path, "r") as f:
            try: users_data = json.load(f)
            except: pass
    users_data.append({"name": user.name, "email": user.email, "role": user.role, "phone": user.phone, "country": user.country, "timestamp": str(datetime.now())})
    with open(backup_path, "w") as f:
        json.dump(users_data, f, indent=4)
        
    return new_user

@app.post("/users/request-otp")
def request_otp(email: str, phone: Optional[str] = None):
    """Generates an OTP and sends it via email/SMS fallback."""
    import random
    otp = str(random.randint(1000, 9999))
    
    # "Always Accessible" Outbox Fallback (Focus on Email for now)
    outbox_path = "backend/data/sms_outbox.log"
    with open(outbox_path, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] To: {email} | OTP: {otp} | Status: LOGGED (Email Only Flow)\n")

    return {
        "message": "OTP processed!", 
        "otp": otp,
        "status": "Email Only"
    }

@app.post("/users/login", response_model=schemas.UserResponse)
def login_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # simple mock login for MVP
    db_user = db.query(models.User).filter(
        models.User.email == user.email, 
        models.User.password == user.password
    ).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return db_user

@app.put("/users/reset-password")
def reset_password(data: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == data.email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.password = data.password
    db.commit()
    return {"message": "Password reset successfully"}

# --- JOB ENDPOINTS ---
@app.post("/jobs", response_model=schemas.JobResponse)
def create_job(job: schemas.JobCreate, hr_id: int, db: Session = Depends(get_db)):
    new_job = models.Job(**job.dict(), hr_id=hr_id)
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job

@app.get("/jobs", response_model=List[schemas.JobResponse])
def get_jobs(db: Session = Depends(get_db)):
    return db.query(models.Job).all()

# --- APPLICATION ENDPOINTS ---
@app.post("/applications", response_model=schemas.ApplicationResponse)
def apply_job(app_data: schemas.ApplicationCreate, candidate_id: int, db: Session = Depends(get_db)):
    # Check if applied
    existing = db.query(models.Application).filter(
        models.Application.job_id == app_data.job_id,
        models.Application.candidate_id == candidate_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already applied to this job")
        
    job = db.query(models.Job).filter(models.Job.id == app_data.job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Run AI Screening
    ai_result = calculate_fit_score(app_data.resume_text, job.requirements)
    
    new_app = models.Application(
        job_id=app_data.job_id,
        candidate_id=candidate_id,
        resume_text=app_data.resume_text,
        ai_score=ai_result["score"],
        ai_feedback=ai_result["feedback"],
        status="Screened" # Auto advanced for MVP showcase
    )
    db.add(new_app)
    db.commit()
    db.refresh(new_app)
    # Persistent Backup (TXT)
    resume_filename = f"backend/data/resumes/app_{new_app.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(resume_filename, "w", encoding="utf-8") as f:
        f.write(f"Candidate ID: {candidate_id}\nJob ID: {new_app.job_id}\nScore: {new_app.ai_score}\n\n{new_app.resume_text}")
        
    return new_app

@app.get("/system/download-data")
def download_data():
    """Zips the data folder and returns it for persistent off-site backup."""
    zip_path = "system_backup"
    shutil.make_archive(zip_path, 'zip', "backend/data")
    return FileResponse(path=f"{zip_path}.zip", filename=f"Nukhba_Backup_{datetime.now().strftime('%Y%m%d')}.zip", media_type='application/zip')

@app.get("/applications/{job_id}", response_model=List[schemas.ApplicationResponse])
def get_applications_for_job(job_id: int, db: Session = Depends(get_db)):
    return db.query(models.Application).filter(models.Application.job_id == job_id).all()

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

# --- SYSTEM ENDPOINTS ---
@app.post("/system/seed")
def seed_database(db: Session = Depends(get_db)):
    # Create HR User
    hr = db.query(models.User).filter(models.User.email == "hr@example.com").first()
    if not hr:
        hr = models.User(name="HR Manager", email="hr@example.com", password="password123", role="HR", country="United Arab Emirates 🇦🇪", phone="+971 50 123 4567")
        db.add(hr)
        db.commit()
        db.refresh(hr)
    
    # Create Candidate
    candidate = db.query(models.User).filter(models.User.email == "candidate@example.com").first()
    if not candidate:
        candidate = models.User(name="John Doe", email="candidate@example.com", password="password123", role="Candidate", country="United Arab Emirates 🇦🇪", phone="+971 50 765 4321")
        db.add(candidate)
        db.commit()
        db.refresh(candidate)

    # Add Sample Jobs
    jobs_data = [
        {
            "title": "Senior Software Engineer",
            "description": "We are looking for a backend pro to join our fintech scaling team.",
            "requirements": "Python, FastAPI, SQLAlchemy, PostgreSQL, Docker, AWS"
        },
        {
            "title": "Product Designer",
            "description": "Design the future of AI interfaces with our creative team.",
            "requirements": "Figma, UI/UX, Design Systems, Prototyping, Adobe Creative Suite"
        },
        {
            "title": "Data Scientist",
            "description": "Leverage LLMs and data to build smart recruitment features.",
            "requirements": "Python, PyTorch, Transformers, NLP, Statistics, Pandas"
        }
    ]
    
    for j in jobs_data:
        existing = db.query(models.Job).filter(models.Job.title == j['title']).first()
        if not existing:
            new_job = models.Job(**j, hr_id=hr.id, status="Open")
            db.add(new_job)
    
    db.commit()
    return {"message": "Database seeded with sample data!"}
