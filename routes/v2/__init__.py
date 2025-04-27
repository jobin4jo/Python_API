from fastapi import APIRouter
from routes.v1 import  user_routes

router = APIRouter()
router.include_router(user_routes.router)