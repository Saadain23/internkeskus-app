from pydantic import BaseModel, Field
from bson import ObjectId
from enum import Enum

class UserRole(str, Enum):
    STUDENT = "student"
    RECRUITER = "recruiter"
    ADMIN = "admin"

class User(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias='_id')
    email: str
    hashed_password: str
    is_active: bool = True
    role: UserRole

    class Config:
        collection = "users"
        arbitrary_types_allowed = True 
