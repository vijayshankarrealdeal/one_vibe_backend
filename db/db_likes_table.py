import sqlalchemy as sa
from database_connect import metadata


likes_table = sa.Table(
    "likes",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("post_id", sa.Integer, sa.ForeignKey("posts.id"), nullable=False),
    sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),

    sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),

    # Optional: ensure a user can only like the same post once
    sa.UniqueConstraint("post_id", "user_id", name="uix_post_user_like"),
)
