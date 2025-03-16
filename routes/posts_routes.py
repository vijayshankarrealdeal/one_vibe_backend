from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request
from services.post_helper import PostHelper
from models.post_model import PostIn, PostOut
from services.auth_helper import oauth2_scheme, is_verified

post_route = APIRouter()


@post_route.post(
    "/create_post",
    dependencies=[Depends(oauth2_scheme)],
    response_model=PostOut,
)
async def create_post(request: Request, post_data: PostIn):
    user_id = request.state.user.id
    if not is_verified(request.state.user):
        raise HTTPException(status_code=401, detail="Unauthorized access")
    if user_id != post_data.user_id:
        raise HTTPException(status_code=401, detail="Unauthorized access")
    post = await PostHelper.create_post(post_data)
    return post


@post_route.get(
    "/get_post", response_model=List[PostOut], dependencies=[Depends(oauth2_scheme)]
)
async def get_post(
    post_id: int = None,
    user_id: int = None,

):
    post = await PostHelper.get_posts(post_id, user_id)
    return post

@post_route.delete(
    "/delete_post",
    dependencies=[Depends(oauth2_scheme)],
)
async def delete_post(request: Request, post_id: int):
    user_id = request.state.user.id
    if not is_verified(request.state.user):
        raise HTTPException(status_code=401, detail="Unauthorized access")
    if post.user_id != user_id:
        raise HTTPException(status_code=401, detail="Unauthorized access")
    post = await PostHelper.delete_post(post_id)
    return post