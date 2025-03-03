from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from core.model import ProjectModel

class ProjectCrud:
    def __init__(self, session:AsyncSession):
        self.session = session

    async def create(self, payload):    
       
        
        db_project = ProjectModel(
            memberid=payload.memberid,
            title=payload.title,
            sub_title=payload.sub_title,
            project_type=payload.project_type,
            project_category=payload.project_category,
            project_tag = payload.project_tag,
            create_data = payload.create_data,
            link=payload.link,
            image=payload.image
        )
        self.session.add(db_project)
        await self.session.commit()
        return db_project
    

    async def get(self):
        
        
        async with self.session as session:  # 비동기 세션 사용
            # 비동기 쿼리 작성
            query = select(ProjectModel).order_by(ProjectModel.create_data.desc())
            
            # 쿼리 실행
            result = await session.execute(query)
            
            # 결과 추출
            projects = result.scalars().all()
            
        return projects
    
