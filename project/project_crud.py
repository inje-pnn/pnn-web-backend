from fastapi import HTTPException
from sqlalchemy import desc
from sqlalchemy.orm import Session
from core.model import ProjectModel


class ProjectCrud:
    def __init__(self, session:Session):
        self.session = session
    
    from sqlalchemy.exc import IntegrityError

    def create(self, payload):
    
        db_projcet = ProjectModel(
            memberid=payload.memberid,
            title=payload.title,
            postdate=payload.postdate,
            project_type=payload.project_type,
            link=payload.link,
            add_content=payload.add_content,
            image=payload.image
        )
        self.session.add(db_projcet)
        self.session.commit()
        return True
    

    def get(self):
        
        projects = self.session.query(ProjectModel).order_by(desc(ProjectModel.postdate)).all()
        
        return projects
    

    def get_by_type(self, payload):
        projects = self.session.query(ProjectModel).filter(
            ProjectModel.project_type == payload.project_type).order_by(desc(
            ProjectModel.postdate)).all()
        
        return projects
    
