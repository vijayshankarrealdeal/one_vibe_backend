from fastapi import APIRouter, BackgroundTasks, Depends, status
from engine import app_user
from models.email_model import EmailSchema, OTPVerifySchema
from models.user_model import UserRegister, UserLogin, UserQueryOut
from services.auth_helper import Auth, oauth2_scheme

user_router = APIRouter(tags=["user"])


@user_router.post("/login", status_code=status.HTTP_200_OK)
async def login(user: UserLogin):
    token = await Auth().login(user)
    return token


@user_router.post("/register",status_code=status.HTTP_201_CREATED)
async def register(user: UserRegister):
    token = await Auth().register(user)
    return token

@user_router.get("/get_user/",status_code=status.HTTP_200_OK, response_model=UserQueryOut, dependencies=[Depends(oauth2_scheme)])
async def get_user_details(id: int):
    user_details = await app_user.get_user(id)
    print(user_details.username)
    return user_details

@user_router.post("/send_otp", status_code=status.HTTP_200_OK)
async def send_otp(background_tasks: BackgroundTasks, email: EmailSchema):
    await Auth().send_verification_email_otp(background_tasks, email)
    return {"message": "OTP sent successfully"}

@user_router.post("/verify_otp", status_code=status.HTTP_200_OK)
async def verify_otp(otp_data: OTPVerifySchema):
    return await Auth().verify_otp(otp_data)
