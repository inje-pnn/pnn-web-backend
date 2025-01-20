from fastapi import APIRouter,Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import provide_session
from project.project_crud import ProjectCrud
from project.project_schema import ProjcetDTO, TypeDTO

project_router = APIRouter(
    prefix="/projcet",
    tags=["project"],
)

@project_router.post("/create")
async def create_project(payload: ProjcetDTO, session:AsyncSession=Depends(provide_session)):
    
    crud=ProjectCrud(session)
    return await crud.create(payload)

@project_router.post("/get")
async def get_projcet(session:AsyncSession=Depends(provide_session)):
    crud=ProjectCrud(session)
    return await crud.get()

@project_router.post("/getbytype")
async def get_projcet_by_type(payload: TypeDTO,session:AsyncSession=Depends(provide_session)):
    crud=ProjectCrud(session)
    return await crud.get_by_type(payload)