from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from User.user_schema import authRequest, UserCreateRequest
from core.database import provide_session
from User.user_crud import UserRepository
from handler.handler import create_access_token, oauth_google
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter( 
    prefix="/user",
    tags=["user"],
)

###
@router.post('/googlelogin')
async def google_login(payload: authRequest, session: AsyncSession = Depends(provide_session)):
    print("Authorization Code:", payload)  # Authorization Code 로그 출력
    code = payload.code
    
    # Google OAuth에서 사용자 정보 가져오기
    user_data = oauth_google(code)
    user_repo = UserRepository(session)
    print(user_data)
    # 사용자가 이미 존재하는 경우
    user = await user_repo.get_user_by_email(user_data.email)
    if user:
        user.token = create_access_token(user_data.email)
        await session.commit()
        return {"access_token": user.token}

    # 신규 사용자 등록
    new_user = await user_repo.create(
        UserCreateRequest(
            name=user_data.name,
            email=user_data.email,
            student_number="placeholder",
            student_grade=0,
            github_url=None,
        )
    )
    new_user.token = create_access_token(new_user.email)
    await session.commit()
    return {"access_token": new_user.token}