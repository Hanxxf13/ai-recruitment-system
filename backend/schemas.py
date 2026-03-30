from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class UserCreate(BaseModel):
    name: str = ""
    email: str
    password: Optional[str] = None
    role: str = "Candidate"
    phone: Optional[str] = None
    country: Optional[str] = None

class GoogleVerifyToken(BaseModel):
    """Receives the raw credential JWT from Google Identity Services."""
    credential: str
    role: Optional[str] = "Candidate"

class GoogleAuthCreate(BaseModel):
    google_id: str
    email: str
    name: str
    avatar_url: Optional[str] = None
    role: Optional[str] = "Candidate"

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    phone: Optional[str] = None
    country: Optional[str] = None
    avatar_url: Optional[str] = None
    auth_provider: Optional[str] = "local"
    resume_text: Optional[str] = None
    auto_apply: bool = False

    class Config:
        from_attributes = True

class JobCreate(BaseModel):
    title: str
    description: str
    requirements: str

class JobResponse(JobCreate):
    id: int
    hr_id: int
    status: str

    class Config:
        from_attributes = True

class ApplicationCreate(BaseModel):
    job_id: int
    resume_text: str

class ApplicationResponse(BaseModel):
    id: int
    job_id: int
    candidate_id: int
    resume_text: str
    status: str
    ai_score: Optional[float]
    ai_feedback: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
