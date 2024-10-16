# app/schemas/student_profile.py

from pydantic import BaseModel, HttpUrl
from typing import List, Optional

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
    profile_picture_url: Optional[HttpUrl] = None
    resume_url: Optional[HttpUrl] = None
    education: List[Education]
    skills: Optional[List[str]] = None
    experience: Optional[List[Experience]] = None
    projects: Optional[List[Project]] = None
    social_links: Optional[List[str]] = None

class StudentProfileCreate(StudentProfileBase):
    pass

class StudentProfileOut(StudentProfileBase):
    user_id: str

    class Config:
        orm_mode = True
