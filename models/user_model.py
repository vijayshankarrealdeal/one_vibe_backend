from typing import Optional
from pydantic import BaseModel

class UserBase(BaseModel):
    email: str

class UserLogin(UserBase):
    password: str

class UserRegister(UserBase):
    password: str

class UserOut(UserBase):
    id: str
    created_at: str
    game_level: str
    