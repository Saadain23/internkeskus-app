from pydantic import BaseModel, GetJsonSchemaHandler
from typing import List, Optional, Any
from pydantic_core import core_schema
from bson import ObjectId

class Education(BaseModel):
    university: str
    degree: str
    graduation_year: int
    gpa: float

class Experience(BaseModel):
    company: str
    position: str
    duration: str
    responsibilities: List[str]

class Project(BaseModel):
    title: str
    description: str
    technologies_used: List[str]
    link: str

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, _source_type: Any, _handler: GetJsonSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.is_instance_schema(ObjectId),
            serialization=core_schema.plain_serializer_function_ser_schema(str),
        )

class StudentProfile(BaseModel):
    user_id: PyObjectId
    first_name: str
    last_name: str
    email: str
    phone_number: Optional[str] = None
    profile_picture_url: Optional[str] = None
    resume_url: Optional[str] = None
    education: List[Education]
    skills: Optional[List[str]] = None
    experience: Optional[List[Experience]] = None
    projects: Optional[List[Project]] = None
    social_links: Optional[List[str]] = None

    class Config:
        collection = "student_profiles"
        arbitrary_types_allowed = True 
        json_encoders = {ObjectId: str}
