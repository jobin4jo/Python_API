from fastapi import APIRouter
from routes.v1 import  user_routes,employee

router = APIRouter()
router.include_router(user_routes.router)
router.include_router(employee.router)
