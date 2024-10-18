# app/api/v1/endpoints/profiles.py

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.schemas.student_profile import StudentProfileOut
from app.schemas.recruiter_profile import RecruiterProfileOut
from app.core.dependencies import get_current_user
from app.models.user import UserRole
from app.services.profile_service import (
    get_student_profile_by_id,
    list_student_profiles,
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

@router.get("/students", response_model=List[StudentProfileOut])
async def list_students(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    name: Optional[str] = Query(None, description="Search by student name (first or last)"),
    university: Optional[str] = Query(None, description="Filter by university"),
    degree: Optional[str] = Query(None, description="Filter by degree"),
    graduation_year: Optional[int] = Query(None, description="Filter by graduation year"),
    skills: Optional[List[str]] = Query(None, description="Filter by skills (comma-separated)"),
    min_gpa: Optional[float] = Query(None, ge=0, le=4, description="Minimum GPA"),
    max_gpa: Optional[float] = Query(None, ge=0, le=4, description="Maximum GPA"),
    company: Optional[str] = Query(None, description="Filter by company in experience"),
    current_user: User = Depends(get_current_user),
):
    if current_user.role not in [UserRole.RECRUITER, UserRole.ADMIN]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    return await list_student_profiles(
        skip=skip,
        limit=limit,
        name=name,
        university=university,
        degree=degree,
        graduation_year=graduation_year,
        skills=skills,
        min_gpa=min_gpa,
        max_gpa=max_gpa,
        company=company,
    )

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
