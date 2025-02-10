from fastapi import APIRouter,Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import provide_session
from project.project_crud import ProjectCrud
from project.project_schema import ProjectDTO, TypeDTO

project_router = APIRouter(
    prefix="/project",
    tags=["project"],
)

@project_router.post("/create")
async def create_project(payload: ProjectDTO, session:AsyncSession=Depends(provide_session)):
    
    crud=ProjectCrud(session)
    return await crud.create(payload)

@project_router.get("/get")
async def get_project(session:AsyncSession=Depends(provide_session)):
    crud=ProjectCrud(session)
    return await crud.get()