from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request
from models.comment_model import CommentIn, CommentOut
from models.likes_model import LikesOut
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
    post = await PostHelper.delete_post(post_id, user_id)
    return post

@post_route.post("/comment_on_post", dependencies=[Depends(oauth2_scheme)])
async def comment_on_post(request: Request, comment_data: CommentIn):
    if not is_verified(request.state.user):
        raise HTTPException(status_code=401, detail="Unauthorized access")
    comment = await PostHelper.comment_on_post(comment_data)
    return comment

@post_route.get(
    "/get_comments",
    response_model=List[CommentOut],
    dependencies=[Depends(oauth2_scheme)],
)
async def get_comments(comment_id: int = None, post_id: int = None):
    comments = await PostHelper.get_comments(comment_id, post_id)
    return comments

@post_route.delete(
    "/delete_comment",
    dependencies=[Depends(oauth2_scheme)],
)
async def delete_comment(request: Request, comment_id: int):
    user_id = request.state.user.id
    if not is_verified(request.state.user):
        raise HTTPException(status_code=401, detail="Unauthorized access")
    comment = await PostHelper.delete_comment(comment_id, user_id)
    return comment

@post_route.post(
    "/like_post",
    dependencies=[Depends(oauth2_scheme)],
)
async def like_post(request: Request, post_id: int):
    user_id = request.state.user.id
    if not is_verified(request.state.user):
        raise HTTPException(status_code=401, detail="Unauthorized access")
    like = await PostHelper.like_post(post_id, user_id)
    return like

@post_route.get(
    "/get_likes",
    dependencies=[Depends(oauth2_scheme)],
    response_model=List[LikesOut]
)
async def get_likes(like_id: int = None, post_id: int = None):
    likes = await PostHelper.get_likes(like_id, post_id)
    return likes

@post_route.delete(
    "/delete_like",
    dependencies=[Depends(oauth2_scheme)],
)
async def delete_like(request: Request, like_id: int):
    user_id = request.state.user.id
    if not is_verified(request.state.user):
        raise HTTPException(status_code=401, detail="Unauthorized access")
    like = await PostHelper.unlike_post(like_id, user_id)
    return like