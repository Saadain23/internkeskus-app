# app/services/profile_service.py

from app.models.student_profile import StudentProfile
from app.models.recruiter_profile import RecruiterProfile
from app.db.mongodb import db
from app.core.config import settings

db_name = settings.PROJECT_NAME

# Student Profile Services
async def get_student_profile(user_id: str):
    profile = await db.client[db_name].student_profiles.find_one({"user_id": user_id})
    return profile

async def get_student_profile_by_id(student_id: str):
    profile = await db.client[db_name].student_profiles.find_one({"user_id": student_id})
    return profile

# Recruiter Profile Services
async def get_recruiter_profile(user_id: str):
    profile = await db.client[db_name].recruiter_profiles.find_one({"user_id": user_id})
    return profile

async def get_recruiter_profile_by_id(recruiter_id: str):
    profile = await db.client[db_name].recruiter_profiles.find_one({"user_id": recruiter_id})
    return profile

async def create_or_update_recruiter_profile(user_id: str, profile_data: dict):
    await db.client[db_name].recruiter_profiles.update_one(
        {"user_id": user_id},
        {"$set": profile_data},
        upsert=True
    )
    updated_profile = await get_recruiter_profile(user_id)
    return updated_profile
