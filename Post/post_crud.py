from sqlalchemy.ext.asyncio import AsyncSession
from Post.post_schema import studyPostDTO, AccountPostDTO
from core.model import StudyPostModel, AccountShareModel
from sqlalchemy.future import select
from typing import List

class studyPostCRUD:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_studyboard(self,*, username, payload:studyPostDTO):

        new_post = StudyPostModel(title=payload.title, 
                             email=payload.email,
                             username = username,
                             project_type =payload.project_type,
                             project_category =payload.project_category,
                             content_link=payload.content_link,
                             image = payload.image,
                             description=payload.description
                             )
        self._session.add(new_post)
        await self._session.commit()
        return new_post
    
    async def get_list_studyboard(self):
        list = await self._session.execute(select(StudyPostModel))
        return list.scalars().all()

    async def get_studyboard_by_serial_number(self, serial_number: int):
        result = await self._session.execute(select(StudyPostModel).filter(StudyPostModel.serial_number == serial_number))
        return result.scalar_one_or_none()

    async def delete_studyboard(self, serial_number: int):
        result = await self._session.execute(select(StudyPostModel).filter(StudyPostModel.serial_number == serial_number))
        post = result.scalar_one_or_none()
        if post:
            await self._session.delete(post)
            await self._session.commit()
            

class AccountPostCRUD:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_Accountboard(self,*,sharername, payload:AccountPostDTO):
        new_post = AccountShareModel(account_id=payload.account_id, 
                             account_password=payload.account_password,
                             sharer=payload.sharer,
                             sharername = sharername,
                             image = payload.image,
                             username=payload.username,
                             description=payload.description
                             )
        self._session.add(new_post)
        await self._session.commit()
        return new_post
    
    async def get_list_accountboard(self):
        list = await self._session.execute(select(AccountShareModel))
        return list.scalars().all()

    async def get_accountboard_by_serial_number(self, serial_number: int):
        result = await self._session.execute(select(AccountShareModel).filter(AccountShareModel.serial_number == serial_number))
        return result.scalar_one_or_none()

    async def delete_accountboard(self, serial_number: int):
        result = await self._session.execute(select(AccountShareModel).filter(AccountShareModel.serial_number == serial_number))
        post = result.scalar_one_or_none()
        if post:
            await self._session.delete(post)
            await self._session.commit()
    
    async def update_accountboard(self, username: List[str], serial_number: int):
        result = await self._session.execute(
            select(AccountShareModel).filter(AccountShareModel.serial_number == serial_number)
        )
        post = result.scalar_one_or_none()
        if post:
            post.username = username
            
            await self._session.commit()
            await self._session.refresh(post)
        
        result = await self._session.execute(select(AccountShareModel).filter(AccountShareModel.serial_number == serial_number))
        return result.scalar_one_or_none()
    
