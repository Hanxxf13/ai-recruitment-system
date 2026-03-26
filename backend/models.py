from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String) # "Admin", "HR", "Candidate"
    
    jobs = relationship("Job", back_populates="hr_user")
    applications = relationship("Application", back_populates="candidate")

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    requirements = Column(String)
    status = Column(String, default="Open")
    hr_id = Column(Integer, ForeignKey("users.id"))
    
    hr_user = relationship("User", back_populates="jobs")
    applications = relationship("Application", back_populates="job")

class Application(Base):
    __tablename__ = "applications"
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    candidate_id = Column(Integer, ForeignKey("users.id"))
    resume_text = Column(String)
    status = Column(String, default="Submitted") # Submitted, Screened, Interviewing, Rejected, Hired
    ai_score = Column(Float, nullable=True) # AI Matching Score
    ai_feedback = Column(String, nullable=True) # Explainable AI Feedback
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    job = relationship("Job", back_populates="applications")
    candidate = relationship("User", back_populates="applications")
