# app/schemas/recruiter_profile.py

from pydantic import BaseModel, HttpUrl
from typing import Optional

class RecruiterProfileBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: Optional[str] = None
    profile_picture_url: Optional[HttpUrl] = None
    position: Optional[str] = None
    company_name: str
    company_description: str
    company_size: str
    company_logo_url: Optional[HttpUrl] = None
    company_location: Optional[str] = None
    company_industry: Optional[str] = None
    company_website: Optional[HttpUrl] = None

class RecruiterProfileCreate(RecruiterProfileBase):
    pass

class RecruiterProfileOut(RecruiterProfileBase):
    user_id: str

    class Config:
        orm_mode = True
