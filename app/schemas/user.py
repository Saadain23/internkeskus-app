# app/schemas/user.py

from pydantic import BaseModel, EmailStr
from enum import Enum

class UserRole(str, Enum):
    STUDENT = "student"
    RECRUITER = "recruiter"
    ADMIN = "admin"

class UserBase(BaseModel):
    email: EmailStr
    role: UserRole

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: str
    is_active: bool

    class Config:
        orm_mode = True
