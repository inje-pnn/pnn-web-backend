from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .user_schema import FirebaseAuthRequest, UserCreateRequest
from core.database import provide_session
from .user_crud import UserRepository

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
            "github_url": user.github_url,
            "authority": user.authority,
        }

    # 기본값 설정
    name = "user"
    student_number = "0"
    student_grade = 0
    github_url = "https://github.com"

    # 사용자 추가
    new_user = await user_repo.create(
        UserCreateRequest(
            name=name,
            email=email,
            student_number=student_number,
            student_grade=student_grade,
            github_url=github_url,
            authority=3,
        )
    )

    return {
        "id": new_user.id,
        "email": new_user.email,
        "name": new_user.name,
        "student_number": new_user.student_number,
        "student_grade": new_user.student_grade,
        "github_url": new_user.github_url,
        "authority": new_user.authority,
    }

@router.put('/approve/{user_id}')
async def approve_user(user_id: int, session: AsyncSession = Depends(provide_session)):
    user_repo = UserRepository(session)

    user = await user_repo.update_authority(user_id=user_id, new_authority=2)
    if not user:
        raise HTTPException(status_code=404, detail="User not found or unable to update authority")

    return {
        "id": user.id,
        "email": user.email,
        "authority": user.authority,
        "message": "User approval successful."
    }

@router.get('/members')
async def get_all_members(session: AsyncSession = Depends(provide_session)):
    user_repo = UserRepository(session)

    users = await user_repo.get_all_users()
    if not users:
        return {"message": "No members found"}

    return [
        {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "student_number": user.student_number,
            "student_grade": user.student_grade,
            "github_url": user.github_url,
            "authority": user.authority,
        }
        for user in users
    ]