###
from pydantic import BaseModel, EmailStr
from typing import Optional

class authRequest(BaseModel):
    code: str

class UserCreateRequest(BaseModel):
    email: EmailStr
    student_number: str
    student_grade: int
    name: str
    github_url: Optional[str] = None

class SocialMember(BaseModel):
    id: Optional[str]
    email: EmailStr
    name: str
    verified_email: Optional[bool]