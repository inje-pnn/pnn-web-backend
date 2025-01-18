from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from .user_schema import FirebaseAuthRequest, UserCreateRequest, authRequest, AddInfoRequest
from core.database import provide_session, get_db
from .user_crud import UserRepository
from handler.handler import create_access_token, oauth_google
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/user",
    tags=["user"],
)

@router.post('/login')
async def login_user(payload: FirebaseAuthRequest, session: AsyncSession = Depends(provide_session)):
    email = payload.email
    user_repo = UserRepository(session)

    # 사용자 확인
    user = await user_repo.get_user_by_email(email)
    if user:
        return {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "student_number": user.student_number,
            "student_grade": user.student_grade,
            "github_url": user.github_url
        }

    # 기본값 설정
    name = payload.name or "user"
    student_number = payload.student_number or "0"
    student_grade = payload.student_grade or 0
    github_url = payload.github_url or "https://github.com"

    # 사용자 추가
    new_user = await user_repo.create(
        UserCreateRequest(
            name=name,
            email=email,
            student_number=student_number,
            student_grade=student_grade,
            github_url=github_url,
        )
    )

    return {
        "id": new_user.id,
        "email": new_user.email,
        "name": new_user.name,
        "student_number": new_user.student_number,
        "student_grade": new_user.student_grade,
        "github_url": new_user.github_url
    }
