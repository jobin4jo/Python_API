from fastapi import APIRouter, Depends

router = APIRouter(prefix="/user", tags=["User"])
@router.get("/",)
async def get_user():
    return "success"