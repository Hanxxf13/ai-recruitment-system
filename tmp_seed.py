import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from database import SessionLocal, engine
import models

def seed():
    # Recreate tables
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Create HR User
        hr = db.query(models.User).filter(models.User.email == "hr@example.com").first()
        if not hr:
            hr = models.User(name="HR Manager", email="hr@example.com", password="password123", role="HR")
            db.add(hr)
            db.commit()
            db.refresh(hr)
        
        # Create Candidate
        candidate = db.query(models.User).filter(models.User.email == "candidate@example.com").first()
        if not candidate:
            candidate = models.User(name="John Doe", email="candidate@example.com", password="password123", role="Candidate")
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
        print("Database seeded successfully with new schema!")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
