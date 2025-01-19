from fastapi import HTTPException
from sqlalchemy import desc
from sqlalchemy.ext.asyncio import AsyncSession
from core.model import ProjectModel
from project.project_schema import ProjcetDTO

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
        
        query = self.session.query(ProjectModel).order_by(desc(ProjectModel.postdate)).all()
        
        result = await self.session.execute(query)
        
        return result
    

    async def get_by_type(self, payload):
        query = self.session.query(ProjectModel).filter(
            ProjectModel.project_type == payload.project_type).order_by(desc(
            ProjectModel.postdate)).all()
        
        result = await self.session.execute(query)
        
        return result
    
