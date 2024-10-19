# app/schemas/student_profile.py

from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId

from app.models.student_profile import PyObjectId

class Education(BaseModel):
    university: str
    degree: str
    graduation_year: int
    gpa: float

class Experience(BaseModel):
    company: str
    position: str
    duration: str
    responsibilities: List[str]

class Project(BaseModel):
    title: str
    description: str
    technologies_used: List[str]
    link: str

class StudentProfileBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: Optional[str] = None
    profile_picture_url: Optional[str] = None
    resume_url: Optional[str] = None
    education: List[Education]
    skills: Optional[List[str]] = None
    experience: Optional[List[Experience]] = None
    projects: Optional[List[Project]] = None
    social_links: Optional[List[str]] = None

class StudentProfileCreate(StudentProfileBase):
    pass

class StudentProfileOut(StudentProfileBase):
    user_id: PyObjectId

    class Config:
        from_attributes = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        
