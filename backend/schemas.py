from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    
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
