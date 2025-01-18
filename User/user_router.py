from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from User.user_schema import FirebaseAuthRequest, UserCreateRequest, authRequest, AddInfoRequest
from core.database import provide_session, get_db
from User.user_crud import UserRepository
from handler.handler import create_access_token, oauth_google
from fastapi.responses import JSONResponse


router = APIRouter(
    prefix="/user",
    tags=["user"],
)

###
@router.post('/googlelogin')
async def googlelogin(payload_oauth: authRequest, session: Session = Depends(get_db)):
    user_repo = UserRepository(session)
    user_data = oauth_google(payload_oauth.code)
    user = user_repo.get_user_by_email(user_data.email)
    if user:
        return create_access_token(user_data.email)
    else:
        user_repo.create(
            UserCreateRequest(
                name=user_data.name,
                email=user_data.email,
                student_id="placeholder",  # 학번 초기값 설정
                year=1,  # 기본 학년 설정
                github_url=None,
            )
        )
        return create_access_token(user_data.email)

@router.post('/add-info')
async def add_info(payload: AddInfoRequest, session: Session = Depends(get_db)):
    user_repo = UserRepository(session)
    user = user_repo.get_user_by_email(payload.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user_repo.update_user_info(
        email=payload.email,
        student_id=payload.student_id,
        year=payload.year,
        github_url=payload.github_url,
    )
    return {"message": "User info updated successfully"}
