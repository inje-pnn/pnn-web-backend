from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session

from core.database import provide_session
from project.project_crud import ProjectCrud
from project.project_schema import ProjcetDTO, TypeDTO

projcetrouter = APIRouter(
    prefix="/projcet",
    tags=["project"],
)

@projcetrouter.post("/create")
def create_project(payload: ProjcetDTO, session:Session=Depends(provide_session)):
    
    crud=ProjectCrud(session)
    return crud.create(payload)

@projcetrouter.post("/get")
def get_projcet(session:Session=Depends(provide_session)):
    crud=ProjectCrud(session)
    return crud.get()

@projcetrouter.post("/getbytype")
def get_projcet_by_type(payload: TypeDTO,session:Session=Depends(provide_session)):
    crud=ProjectCrud(session)
    return crud.get_by_type(payload)