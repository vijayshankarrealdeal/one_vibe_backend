from datetime import datetime
from pydantic import BaseModel


class CommentOut(BaseModel):
    comment_id: int
    user_id: int
    text: str
    created_at: datetime