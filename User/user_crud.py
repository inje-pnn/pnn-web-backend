###
from sqlalchemy.future import select
from core.model import UserModel
from sqlalchemy.ext.asyncio import AsyncSession

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_create_request):
        new_user = UserModel(
            name=user_create_request.name,
            email=user_create_request.email,
            student_number=user_create_request.student_number,
            student_grade=user_create_request.student_grade,
            github_url=user_create_request.github_url,
            authority=user_create_request.authority or 3
        )
        self.session.add(new_user)
        await self.session.commit()
        return new_user

    async def get_user_by_email(self, email: str):
        stmt = select(UserModel).where(UserModel.email == email)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def update_authority(self, user_id: int, new_authority: int):
        stmt = select(UserModel).where(UserModel.id == user_id)
        result = await self.session.execute(stmt)
        user = result.scalars().first()

        if not user:
            return None

        user.authority = new_authority
        await self.session.commit()
        return user
    
    async def get_all_users(self):
        stmt = select(UserModel)
        result = await self.session.execute(stmt)
        return result.scalars().all()