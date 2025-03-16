from datetime import datetime
from pydantic import BaseModel

class LikesOut(BaseModel):
    likes_id: int
    user_id: int
    created_at : datetime