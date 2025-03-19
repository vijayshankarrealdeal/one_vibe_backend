from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class CommentOut(BaseModel):
    comment_id: int
    user_id: int
    text: str
    created_at: datetime
    updated_at: datetime

from pydantic import BaseModel, Field, root_validator
from datetime import datetime
from typing import Optional

class CommentOut(BaseModel):
    comment_id: int = Field(alias="comment_id_table")
    user_id: int = Field(alias="user_comment_id")
    text: str = Field(alias="comment_text")
    created_at: datetime = Field(alias="comment_created_at")
    updated_at: datetime = Field(alias="comment_updated_at")
    class Config:
        populate_by_name = True 

class CommentIn(BaseModel):
    post_comment_id: int
    user_comment_id: int
    comment_text: str
