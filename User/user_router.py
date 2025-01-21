from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .user_schema import FirebaseAuthRequest, UserCreateRequest
from .user_crud import UserRepository
from core.database import provide_session
from core.model import UserModel


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

from fastapi import Body  # Body를 사용하여 요청에서 권한 값을 받음

@router.put('/approve/{user_id}')
async def approve_user(
    user_id: int,
    new_authority: int = Body(..., description="New authority level for the user"),
    session: AsyncSession = Depends(provide_session),
):
    user_repo = UserRepository(session)

    user = await user_repo.update_authority(user_id=user_id, new_authority=new_authority)
    if not user:
        raise HTTPException(status_code=404, detail="User not found or unable to update authority")

    return {
        "id": user.id,
        "email": user.email,
        "authority": user.authority,
        "message": f"User authority updated to {new_authority}."
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


@router.put('/update/{user_id}')
async def update_user_info(
    user_id: int,
    name: str = Body(None, description="New name of the user"),
    student_number: str = Body(None, description="New student number"),
    student_grade: int = Body(None, description="New student grade"),
    github_url: str = Body(None, description="New GitHub URL"),
    session: AsyncSession = Depends(provide_session),
):
    user_repo = UserRepository(session)

    stmt = select(UserModel).where(UserModel.id == user_id)
    result = await session.execute(stmt)
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if name is not None:
        user.name = name
    if student_number is not None:
        user.student_number = student_number
    if student_grade is not None:
        user.student_grade = student_grade
    if github_url is not None:
        user.github_url = github_url

    await session.commit()

    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "student_number": user.student_number,
        "student_grade": user.student_grade,
        "github_url": user.github_url,
        "authority": user.authority,
        "message": "User information updated successfully."
    }
