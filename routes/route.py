from fastapi import APIRouter
from routes.user_auth_route import user_router
from routes.photo_upload_route import photo_upload_router
from routes.posts_routes import post_route

router = APIRouter()
router.include_router(user_router, prefix="/user", tags=["user"])
router.include_router(photo_upload_router, prefix="/images", tags=["images"])
router.include_router(post_route, prefix="/posts", tags=["posts"])