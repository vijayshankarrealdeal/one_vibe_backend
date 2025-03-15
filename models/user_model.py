from typing import Optional
from pydantic import BaseModel
import datetime
class UserBase(BaseModel):
    username: str
    is_verified: Optional[bool] = False

class UserLogin(UserBase):
    password: str

class UserRegister(UserBase):
    name: str
    password: str
    email: str

class UserOut(UserBase):
    id: str
    created_at: str
    user_rank: str

class UserQueryOut(UserBase):
    id: int
    email: Optional[str]
    name: Optional[str]
    profile_picture: Optional[str]
    bio: Optional[str]
    user_type: Optional[str]
    user_rank: Optional[str]
    created_at: Optional[datetime.datetime]

class UserUpdate(BaseModel):
    id: int
    name: Optional[str] = None
    profile_picture: Optional[str] = None
    bio: Optional[str] = None