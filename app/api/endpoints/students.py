# app/api/v1/endpoints/students.py

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import RedirectResponse
from app.schemas.user import UserOut
from app.schemas.student_profile import StudentProfileCreate, StudentProfileOut
from app.core.dependencies import get_current_user
from app.models.user import UserRole
from app.services.blob_storage_service import upload_file_to_blob, get_file_url
from app.services.profile_service import (
    get_student_profile,
    create_or_update_student_profile,
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

@router.post("/me/create-update-profile", response_model=StudentProfileOut)
async def create_update_my_profile(
    profile_data: StudentProfileCreate,
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.STUDENT:
        raise HTTPException(status_code=403, detail="Not authorized")
    updated_profile = await create_or_update_student_profile(current_user.id, profile_data)
    return updated_profile

# Student Profile file handling

@router.post("/me/upload-resume")
async def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != UserRole.STUDENT:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    file_extension = file.filename.split(".")[-1]
    file_name = f"resumes/{current_user.id}-{file.filename.split(".")[0]}.{file_extension}"
    file_content = await file.read()
    
    await upload_file_to_blob(file_name, file_content, file.content_type)
    
    # Update the student profile with the new resume file name
    profile = await get_student_profile(current_user.id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    profile.resume_file_name = file_name
    updated_profile = await create_or_update_student_profile(current_user.id, profile)
    
    return {"message": "Resume uploaded successfully"}


@router.post("/me/upload-profile-picture")
async def upload_profile_picture(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != UserRole.STUDENT:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    file_extension = file.filename.split(".")[-1]
    file_name = f"profile_pictures/{current_user.id}-{file.filename.split(".")[0]}.{file_extension}"
    file_content = await file.read()
    
    await upload_file_to_blob(file_name, file_content, file.content_type)
    
    # Update the student profile with the new profile picture file name
    profile = await get_student_profile(current_user.id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    profile.profile_picture_file_name = file_name
    updated_profile = await create_or_update_student_profile(current_user.id, profile)
    
    return {"message": "Profile picture uploaded successfully"}

@router.get("/me/resume")
async def get_resume(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.STUDENT:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    profile = await get_student_profile(current_user.id)
    if not profile or not profile.resume_file_name:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    resume_url = await get_file_url(profile.resume_file_name)
    return RedirectResponse(url=resume_url)

@router.get("/me/profile-picture")
async def get_profile_picture(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.STUDENT:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    profile = await get_student_profile(current_user.id)
    if not profile or not profile.profile_picture_file_name:
        raise HTTPException(status_code=404, detail="Profile picture not found")
    
    profile_picture_url = await get_file_url(profile.profile_picture_file_name)
    return RedirectResponse(url=profile_picture_url)