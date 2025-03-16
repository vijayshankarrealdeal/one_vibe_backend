import sqlalchemy as sa
from database_connect import metadata


db_likes_table = sa.Table(
    "likes",
    metadata,
    sa.Column("likes_id_table", sa.Integer, primary_key=True),
    sa.Column("post_like_id", sa.Integer, sa.ForeignKey("posts.post_id_table"), nullable=False),
    sa.Column("user_like_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),

    sa.Column("likes_created_at", sa.DateTime, server_default=sa.func.now()),

    # Optional: ensure a user can only like the same post once
    sa.UniqueConstraint("post_like_id", "user_like_id", name="uix_post_user_like"),
)
