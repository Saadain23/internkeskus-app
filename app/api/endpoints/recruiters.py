# app/api/v1/endpoints/recruiters.py

from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user import UserOut
from app.schemas.recruiter_profile import RecruiterProfileCreate, RecruiterProfileOut
from app.core.dependencies import get_current_user
from app.models.user import UserRole
from app.services.profile_service import (
    create_or_update_recruiter_profile,
    get_recruiter_profile
)
from app.models.user import User

router = APIRouter()

@router.get("/me", response_model=UserOut)
async def read_current_recruiter(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.RECRUITER:
        raise HTTPException(status_code=403, detail="Not authorized")
    return current_user

@router.get("/me/profile", response_model=RecruiterProfileOut)
async def get_my_profile(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.RECRUITER:
        raise HTTPException(status_code=403, detail="Not authorized")
    profile = await get_recruiter_profile(current_user.id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.post("/me/profile", response_model=RecruiterProfileOut)
async def create_update_my_profile(
    profile_data: RecruiterProfileCreate,
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.RECRUITER:
        raise HTTPException(status_code=403, detail="Not authorized")
    profile = await create_or_update_recruiter_profile(current_user.id, profile_data.dict())
    return profile

