import sqlalchemy as sa
from database_connect import metadata


db_comments_table = sa.Table(
    "comments",
    metadata,
    sa.Column("comment_id_table", sa.Integer, primary_key=True),
    sa.Column("post_comment_id", sa.Integer, sa.ForeignKey("posts.post_id_table"), nullable=False),
    sa.Column("user_comment_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
    sa.Column("comment_text", sa.Text, nullable=False),

    sa.Column("comment_created_at", sa.DateTime, server_default=sa.func.now()),
    sa.Column("comment_updated_at", sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now()),
)

