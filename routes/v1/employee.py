from fastapi import APIRouter, Depends
from logger import logger
router = APIRouter(prefix="/employee", tags=["emp"])
@router.get("/",)
async def get_employee():
    logger.info("Root endpoint accessed")
    logger.info("Root endpoint 00")
    return "success"