# app/api/v1/endpoints/students.py

from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user import UserOut
from app.schemas.student_profile import StudentProfileCreate, StudentProfileOut
from app.core.dependencies import get_current_user
from app.models.user import UserRole
from app.services.profile_service import (
    get_student_profile
)
from app.models.user import User

router = APIRouter()

@router.get("/me", response_model=UserOut)
async def read_current_student(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.STUDENT:
        raise HTTPException(status_code=403, detail="Not authorized")
    return {
        "id": str(current_user.id),  # Convert ObjectId to string if necessary
        "email": current_user.email,
        "is_active": current_user.is_active,
        "role": current_user.role,
    }

@router.get("/me/profile", response_model=StudentProfileOut)
async def get_my_profile(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.STUDENT:
        raise HTTPException(status_code=403, detail="Not authorized")
    profile = await get_student_profile(current_user.id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

