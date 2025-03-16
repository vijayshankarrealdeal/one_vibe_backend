import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ARRAY
from database_connect import metadata

db_posts_table = sa.Table(
    "posts",
    metadata,
    sa.Column("post_id_table", sa.Integer, primary_key=True),
    sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
    sa.Column("post_text", sa.Text, nullable=True),
    # Store a list of image URLs or paths as a PostgreSQL array of text
    sa.Column("post_images", ARRAY(sa.String), nullable=True),
    # Share count can be stored as an integer, default 0
    sa.Column("post_share_count", sa.Integer, server_default="0", nullable=False),
    sa.Column("created_post_at", sa.DateTime, server_default=sa.func.now()),
    sa.Column("updated_post_at", sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now()),
)

