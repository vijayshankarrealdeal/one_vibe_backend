from fastapi import APIRouter
from routes.user_auth import user_router

router = APIRouter()
router.include_router(user_router, prefix="/user", tags=["user"])
