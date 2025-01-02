from fastapi import APIRouter

router = APIRouter(
    prefix="/user",
    tags=["user"],
)

@router.get("/")
async def hi():
    return "hi"