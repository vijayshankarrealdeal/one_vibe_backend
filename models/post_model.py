from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from models.user_model import UserQueryOut
from models.likes_model import LikesOut
from models.comment_model import CommentOut


class PostIn(BaseModel):
    user_id: int
    post_text: str
    post_images: Optional[List[str]] = []
    post_share_count: int = 0

class PostOut(BaseModel):
    post_id_table: int
    user: UserQueryOut
    post_text: str
    post_images: Optional[List[str]] = []
    post_share_count: int = 0
    created_post_at: datetime
    likes: Optional[List[LikesOut]] = []
    comments: Optional[List[CommentOut]] = []
