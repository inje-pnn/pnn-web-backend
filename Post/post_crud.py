from sqlalchemy.ext.asyncio import AsyncSession
from .post_schema import studyPostDTO, AccountPostDTO
from core.models import StudyPostModel, AccountShareModel
from sqlalchemy.future import select

class studyPostCRUD:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_studyboard(self,*,payload:studyPostDTO):
        new_post = StudyPostModel(title=payload.title, 
                             user_id=payload.user_id,
                             type=payload.type,
                             content_link=payload.content_link,
                             )
        self._session.add(new_post)
        await self._session.commit()
        return new_post
    
    async def get_list_studyboard(self):
        list = await self._session.execute(select(StudyPostModel))
        return list.scalars().all()

    async def get_studyboard_by_id(self, post_id: int):
        result = await self._session.execute(select(StudyPostModel).filter(StudyPostModel.serial_number == post_id))
        return result.scalar_one_or_none()

    async def delete_studyboard(self, post_id: int):
        result = await self._session.execute(select(StudyPostModel).filter(StudyPostModel.serial_number == post_id))
        post = result.scalar_one_or_none()
        if post:
            await self._session.delete(post)
            await self._session.commit()

class AccountPostCRUD:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_Accountboard(self,*,payload:AccountPostDTO):
        new_post = AccountShareModel(account_id=payload.account_id, 
                             account_password=payload.account_password,
                             sharer=payload.sharer,
                             username=payload.username,
                             )
        self._session.add(new_post)
        await self._session.commit()
        return new_post
    
    async def get_list_accountboard(self):
        list = await self._session.execute(select(AccountShareModel))
        return list.scalars().all()

    async def get_accountboard_by_id(self, post_id: int):
        result = await self._session.execute(select(AccountShareModel).filter(AccountShareModel.serial_number == post_id))
        return result.scalar_one_or_none()

    async def delete_accountboard(self, post_id: int):
        result = await self._session.execute(select(AccountShareModel).filter(AccountShareModel.serial_number == post_id))
        post = result.scalar_one_or_none()
        if post:
            await self._session.delete(post)
            await self._session.commit()
    
