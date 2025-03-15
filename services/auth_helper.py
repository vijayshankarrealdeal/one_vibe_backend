from typing import Optional
import jwt
import datetime
from fastapi import BackgroundTasks, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import HTTPException
from database_connect import dbs, redis_client
from db.db_user_table import db_user_table
from models.email_model import EmailSchema, OTPVerifySchema
from models.user_model import UserLogin, UserQueryOut, UserRegister, UserUpdate
from op_logging import logging
from passlib.context import CryptContext
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

from utils import generate_otp, is_rate_limiter, track_fail_attemps

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Auth:
    @staticmethod
    def encode_token(user_data):
        payload = {
            "exp": datetime.datetime.now() + datetime.timedelta(days=12),
            "sub": str(user_data["id"]),
        }
        try:
            token = jwt.encode(payload, "XYZ", algorithm="HS256")
            return {"token": token}
        except Exception as e:
            logging.debug(f"Error in encoding token: {e}")
            raise HTTPException(status_code=400, detail="Unkonwn error")

    @staticmethod
    async def get_user(user_id):
        try:
            user_data = await dbs.fetch_one(
                db_user_table.select().where(db_user_table.c.id == user_id)
            )
            return user_data
        except HTTPException as e:
            logging.debug(f"Error in registering user: {e}")
            raise HTTPException(status_code=400, detail="Unkonwn error")

    async def register(self, user_data: UserRegister):
        user_data.password = pwd_context.hash(user_data.password)
        query = db_user_table.insert().values(**user_data.model_dump())
        async with dbs.transaction() as transaction:
            user_id = await transaction._connection.execute(query)
            user_data = await self.get_user(user_id)
            return self.encode_token(user_data)

    async def login(self, user_data: UserLogin):

        query = db_user_table.select().where(
            db_user_table.c.username == user_data.username
        )
        user_id = await dbs.execute(query)
        if not user_id:
            raise HTTPException(status_code=400, detail="Invalid email or password")
        user_db_data = await dbs.fetch_one(
            db_user_table.select().where(db_user_table.c.id == user_id)
        )
        if not pwd_context.verify(user_data.password, user_db_data.password):
            raise HTTPException(status_code=400, detail="Invalid email or password")
        return self.encode_token(user_db_data)

    @staticmethod
    async def send_verification_email_otp(
        background_tasks: BackgroundTasks, email_data: EmailSchema
    ):
        if is_rate_limiter(email_data.email):
            raise HTTPException(
                status_code=429, detail="Too many OTP requests. Try again later."
            )

        MAIL_CONFIG = {
            "MAIL_USERNAME": "vijaygaya056@gmail.com",
            "MAIL_PASSWORD": "rroqgefuuhawxvbk",
            "MAIL_FROM": "vijaygaya056@gmail.com",
            "MAIL_PORT": 587,
            "MAIL_SERVER": "smtp.gmail.com",
            "MAIL_STARTTLS": True,  # Updated field
            "MAIL_SSL_TLS": False,  # Updated field
        }

        conf = ConnectionConfig(
            MAIL_USERNAME=MAIL_CONFIG["MAIL_USERNAME"],
            MAIL_PASSWORD=MAIL_CONFIG["MAIL_PASSWORD"],
            MAIL_FROM=MAIL_CONFIG["MAIL_FROM"],
            MAIL_PORT=MAIL_CONFIG["MAIL_PORT"],
            MAIL_SERVER=MAIL_CONFIG["MAIL_SERVER"],
            MAIL_STARTTLS=MAIL_CONFIG["MAIL_STARTTLS"],  # Updated
            MAIL_SSL_TLS=MAIL_CONFIG["MAIL_SSL_TLS"],  # Updated
            USE_CREDENTIALS=True,
        )
        otp = generate_otp()
        otp_key = f"otp:{email_data.email}"
        redis_client.setex(otp_key, 300, otp)
        message = MessageSchema(
            subject="Your OTP Code",
            recipients=[email_data.email],
            body=f"""
        <h3>Your OTP Code</h3>
        <p>Your One-Time Password (OTP) is: <strong>{otp}</strong></p>
        <p>This OTP will expire in 5 minutes.</p>
        """,
            subtype="html",
        )
        fm = FastMail(conf)
        background_tasks.add_task(fm.send_message, message)

    @staticmethod
    async def verify_otp(otp_data: OTPVerifySchema):
        otp_key = f"otp:{otp_data.email}"
        stored_otp = redis_client.get(otp_key)

        # 🛑 **Check if OTP exists**
        if stored_otp is None:
            raise HTTPException(status_code=400, detail="OTP expired or not found")

        # 🛑 **Check Brute Force Protection**
        if (
            redis_client.get(f"failed_attempts:{otp_data.email}")
            and int(redis_client.get(f"failed_attempts:{otp_data.email}")) >= 5
        ):
            raise HTTPException(
                status_code=403, detail="Too many incorrect attempts. Try again later."
            )

        # 🔐 **Verify OTP**
        if otp_data.otp != stored_otp:
            if track_fail_attemps(otp_data.email):  # Check if user should be blocked
                raise HTTPException(
                    status_code=403,
                    detail="Too many incorrect attempts. Try again later.",
                )
            raise HTTPException(status_code=400, detail="Invalid OTP")

        # ✅ **Successful Verification: Clear OTP & Attempts**
        await dbs.execute(
            db_user_table.update()
            .where(db_user_table.c.username == otp_data.username)
            .values({"is_verified": True, "email": otp_data.email})
        )
        redis_client.delete(otp_key)
        redis_client.delete(f"failed_attempts:{otp_data.email}")

        return {"message": True}

    @staticmethod
    async def update_password(user_id: int, password: str):
        hashed_password = pwd_context.hash(password)
        query = (
            db_user_table.update()
            .where(db_user_table.c.id == user_id)
            .values({"password": hashed_password})
        )
        return await dbs.execute(query)

    @staticmethod
    async def update_user(usr_id, user_data: UserUpdate):
        user_dict = user_data.model_dump(exclude_none=True)
        user_dict.pop("id")
        query = (
            db_user_table.update()
            .where(db_user_table.c.id == usr_id)
            .values(user_dict)
        )
        await dbs.execute(query)
        user_data = await Auth().get_user(usr_id)
        return user_data


class CustomHTTPBearer(HTTPBearer):
    async def __call__(
        self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        res = await super().__call__(request)
        try:
            payload = jwt.decode(res.credentials, "XYZ", algorithms=["HS256"])
            user_data = await dbs.fetch_one(
                db_user_table.select().where(db_user_table.c.id == int(payload["sub"]))
            )
            if not user_data:
                raise HTTPException(401, "Invalid token")
            request.state.user = user_data
            return request
        except jwt.ExpiredSignatureError:
            raise HTTPException(401, "Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(401, "Invalid token")


oauth2_scheme = CustomHTTPBearer()


def is_verified(user):
    if user["is_verified"]:
        return True
    raise HTTPException(401, "User not verified.")


def get_current_user_id(request: Request) -> str:
    if not hasattr(request.state, "id") or request.state.id is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return request.state.id


def is_admin(request):
    if request.state.user["user_type"] == "ADMIN":
        return True
    raise HTTPException(401, "You are not authorized.")
