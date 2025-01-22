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
            postdate=payload.postdate,
            project_type=payload.project_type,
            link=payload.link,
            add_content=payload.add_content,
            image=payload.image
        )
        self.session.add(db_project)
        await self.session.commit()
        return db_project
    

    async def get(self):
        
        
        async with self.session as session:  # 비동기 세션 사용
            # 비동기 쿼리 작성
            query = select(ProjectModel).order_by(ProjectModel.postdate.desc())
            
            # 쿼리 실행
            result = await session.execute(query)
            
            # 결과 추출
            projects = result.scalars().all()
            
        return projects
    

    async def get_by_type(self, payload):
        query = select(ProjectModel).filter(
            ProjectModel.project_type == payload.project_type).order_by(desc(
            ProjectModel.postdate))
        
        result = await self.session.execute(query)

        projects = result.scalars().all()
        
        return projects
    
