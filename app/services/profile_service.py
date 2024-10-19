# app/services/profile_service.py

from typing import List, Optional
from app.models.student_profile import StudentProfile
from app.models.recruiter_profile import RecruiterProfile
from app.db.mongodb import db
from app.core.config import settings
from app.schemas.student_profile import StudentProfileCreate

db_name = settings.PROJECT_NAME

# Student Profile Services
async def get_student_profile(user_id: str):
    profile = await db.client[db_name].student_profiles.find_one({"user_id": user_id})
    return profile

async def list_student_profiles(
    skip: int,
    limit: int,
    name: Optional[str] = None,
    university: Optional[str] = None,
    degree: Optional[str] = None,
    graduation_year: Optional[int] = None,
    skills: Optional[List[str]] = None,
    min_gpa: Optional[float] = None,
    max_gpa: Optional[float] = None,
    company: Optional[str] = None,
)-> List[StudentProfile]:

    collection = db.client[db_name].student_profiles

    filter_query = {}

    if name:
        filter_query["$or"] = [
            {"first_name": {"$regex": name, "$options": "i"}},
            {"last_name": {"$regex": name, "$options": "i"}}
        ]
    if university:
        filter_query["education.university"] = {"$regex": university, "$options": "i"}
    if degree:
        filter_query["education.degree"] = {"$regex": degree, "$options": "i"}
    if graduation_year:
        filter_query["education.graduation_year"] = graduation_year
    if skills:
        filter_query["skills"] = {"$all": skills}
    if min_gpa is not None or max_gpa is not None:
        gpa_query = {}
        if min_gpa is not None:
            gpa_query["$gte"] = min_gpa
        if max_gpa is not None:
            gpa_query["$lte"] = max_gpa
        filter_query["education.gpa"] = gpa_query
    if company:
        filter_query["experience.company"] = {"$regex": company, "$options": "i"}

    cursor = collection.find(filter_query).skip(skip).limit(limit)
    return [StudentProfile(**doc) for doc in await cursor.to_list(length=limit)]
    

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

async def create_or_update_student_profile(user_id: str, profile_data: StudentProfileCreate):

    await db.client[db_name].student_profiles.update_one(
        {"user_id": user_id},
        {"$set": profile_data},
        upsert=True
    )
    updated_profile = await get_student_profile(user_id)
    return updated_profile

async def create_or_update_recruiter_profile(user_id: str, profile_data: dict):
    await db.client[db_name].recruiter_profiles.update_one(
        {"user_id": user_id},
        {"$set": profile_data},
        upsert=True
    )
    updated_profile = await get_recruiter_profile(user_id)
    return updated_profile
