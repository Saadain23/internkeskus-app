# app/models/recruiter_profile.py

from pydantic import BaseModel, HttpUrl
from typing import Optional
from bson import ObjectId
class RecruiterProfile(BaseModel):
    user_id: str
    first_name: str
    last_name: str
    company_email: str
    phone_number: Optional[str] = None
    profile_picture_url: Optional[HttpUrl] = None
    position: Optional[str] = None
    company_name: str
    company_description: str
    company_size: str
    company_logo_url: Optional[HttpUrl] = None
    company_location: Optional[str] = None
    company_industry: Optional[str] = None
    company_website: Optional[str] = None

    class Config:
        collection = "recruiter_profiles"
        arbitrary_types_allowed = True 
