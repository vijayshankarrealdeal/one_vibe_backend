from typing import Optional
import jwt
import datetime
from fastapi import Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import HTTPException
from database_connect import dbs
from db.db_user_table import db_user_table
from models.user_model import UserLogin, UserRegister
from op_logging import logging
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Auth:
    @staticmethod
    def encode_token(user_data):
        payload = {
            "exp": datetime.datetime.now() + datetime.timedelta(days=12),
            "sub": str(user_data['id']),
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

        query = db_user_table.select().where(db_user_table.c.email == user_data.email)
        user_id = await dbs.execute(query)
        if not user_id:
            raise HTTPException(status_code=400, detail="Invalid email or password")
        user_db_data = await dbs.fetch_one(
            db_user_table.select().where(db_user_table.c.id == user_id)
        )
        if not pwd_context.verify(user_data.password,user_db_data.password):
            raise HTTPException(status_code=400, detail="Invalid email or password")
        return self.encode_token(user_db_data)


class CustomHTTPBearer(HTTPBearer):
    async def __call__(self, request: Request) -> Optional[HTTPAuthorizationCredentials]:
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


def is_admin(request):
    if request.state.user["user_type"] == "ADMIN":
        return True
    raise HTTPException(401, "You are not authorized.")
