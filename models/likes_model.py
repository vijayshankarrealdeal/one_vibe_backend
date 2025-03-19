from datetime import datetime
from pydantic import BaseModel, Field

class LikesOut(BaseModel):
    likes_id: int = Field(alias="likes_id_table")
    user_id: int = Field(alias="user_like_id")
    created_at : datetime = Field(alias="likes_created_at")
    class Config:
        populate_by_name = True 