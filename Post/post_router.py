from fastapi import APIRouter, Depends, HTTPException
from core.database import provide_session
from sqlalchemy.ext.asyncio import AsyncSession
from User.user_crud import UserRepository
from Post.post_schema import studyPostDTO, AccountPostDTO
from Post.post_crud import studyPostCRUD, AccountPostCRUD

router = APIRouter(
    prefix="/post",
    tags=["post"],
)

@router.post("/post_studyboard")
async def post_studyboard(PDTO: studyPostDTO, db: AsyncSession = Depends(provide_session)):
    UserCrud = UserRepository(db)
    user = await UserCrud.get_user_by_email(PDTO.email)

    if user is None:
        return {"message" : "email이 존재하지 않습니다."}
    
    crud = studyPostCRUD(db)
    post = await crud.create_studyboard(payload=PDTO)
    return post

@router.get("/get_studyboardlist")
async def get_studyboardlist(db: AsyncSession = Depends(provide_session)):
    crud = studyPostCRUD(db)
    studyboards = await crud.get_list_studyboard()
    return studyboards

@router.delete("/delete_studyboard/{serial_number}")
async def delete_studyboard(serial_number: int, db: AsyncSession = Depends(provide_session)):
    crud = studyPostCRUD(db)

    post = await crud.get_studyboard_by_serial_number(serial_number)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    await crud.delete_studyboard(serial_number)
    return {"message": "Post deleted successfully"}

@router.post("/post_Accountboard")
async def post_Accountboard(ADTO: AccountPostDTO, db: AsyncSession = Depends(provide_session)):
    UserCrud = UserRepository(db)
    user = await UserCrud.get_user_by_email(ADTO.sharer)

    if user is None:
        return {"message" : "email이 존재하지 않습니다."}
    else:
        crud = AccountPostCRUD(db)
        post = await crud.create_Accountboard(payload=ADTO)
        return post
    

@router.get("get_accountboardlist")
async def get_studyboardlist(db: AsyncSession = Depends(provide_session)):
    crud = AccountPostCRUD(db)
    accountboards = await crud.get_list_accountboard()
    return accountboards

@router.delete("/delete_accountboard/{serial_number}")
async def delete_studyboard(serial_number: int, db: AsyncSession = Depends(provide_session)):
    crud = AccountPostCRUD(db)

    post = await crud.get_accountboard_by_serial_number(serial_number)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    await crud.delete_accountboard(serial_number)
    return {"message": "Post deleted successfully"}