from fastapi import APIRouter, status
from models.user_model import UserRegister, UserLogin
from services.auth_helper import Auth

user_router = APIRouter(tags=["user"])


@user_router.post("/login", status_code=status.HTTP_200_OK)
async def login(user: UserLogin):
    token = await Auth().login(user)
    return token


@user_router.post("/register",status_code=status.HTTP_201_CREATED)
async def register(user: UserRegister):
    token = await Auth().register(user)
    return token
