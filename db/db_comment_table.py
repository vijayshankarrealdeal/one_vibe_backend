import sqlalchemy as sa
from database_connect import metadata


comments_table = sa.Table(
    "comments",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("post_id", sa.Integer, sa.ForeignKey("posts.id"), nullable=False),
    sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
    sa.Column("text", sa.Text, nullable=False),

    sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    sa.Column("updated_at", sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now()),
)

