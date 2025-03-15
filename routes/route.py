from fastapi import APIRouter
from routes.user_auth import user_router
from routes.photo_upload import photo_upload_router

router = APIRouter()
router.include_router(user_router, prefix="/user", tags=["user"])
router.include_router(photo_upload_router, prefix="/images", tags=["images"])
