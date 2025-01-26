###
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreateRequest(BaseModel):
    email: EmailStr
    student_number: str
    student_grade: int
    name: str
    github_url: Optional[str] = None
    authority: Optional[int] = 2

class FirebaseAuthRequest(BaseModel):
    email: EmailStr