###
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreateRequest(BaseModel):
    email: EmailStr
    student_number: str
    student_grade: int
    name: str
    github_url: Optional[str] = None
    authority: Optional[int] = 3

class FirebaseAuthRequest(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    student_number: Optional[str] = None
    student_grade: Optional[int] = None
    github_url: Optional[str] = None