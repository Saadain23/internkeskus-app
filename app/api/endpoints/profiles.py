# app/api/v1/endpoints/profiles.py

from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.student_profile import StudentProfileOut
from app.schemas.recruiter_profile import RecruiterProfileOut
from app.core.dependencies import get_current_user
from app.models.user import UserRole
from app.services.profile_service import (
    get_student_profile_by_id,
    get_recruiter_profile_by_id,
)
from app.models.user import User

router = APIRouter()

@router.get("/students/{student_id}", response_model=StudentProfileOut)
async def get_student_profile(
    student_id: str,
    current_user: User = Depends(get_current_user),
):
    # Only recruiters or admins can view student profiles by ID
    if current_user.role not in [UserRole.RECRUITER, UserRole.ADMIN]:
        raise HTTPException(status_code=403, detail="Not authorized")
    profile = await get_student_profile_by_id(student_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Student profile not found")
    return profile

@router.get("/recruiters/{recruiter_id}", response_model=RecruiterProfileOut)
async def get_recruiter_profile(
    recruiter_id: str,
    current_user: User = Depends(get_current_user),
):
    # Only students or admins can view recruiter profiles by ID
    if current_user.role not in [UserRole.STUDENT, UserRole.ADMIN]:
        raise HTTPException(status_code=403, detail="Not authorized")
    profile = await get_recruiter_profile_by_id(recruiter_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Recruiter profile not found")
    return profile
