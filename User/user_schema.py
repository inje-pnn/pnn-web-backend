###
from typing import Optional
from pydantic import BaseModel, EmailStr

class authRequest(BaseModel):
    code:str

class SocialMember(BaseModel):
    name :str
    email: str

class UserCreateRequest(BaseModel):
    email: EmailStr  # 이메일 형식 자동 검증
    student_id: str  # 학번
    year: int        # 학년
    name: str        # 이름
    github_url: Optional[str] = None  # 선택적 필드

class AddInfoRequest(BaseModel):
    email: EmailStr
    student_id: str
    year: int
    github_url: Optional[str] = None