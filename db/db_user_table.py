import sqlalchemy as sa
from db.db_enmus import UserType, UserRank
from database_connect import metadata

db_user_table = sa.Table(
    "users",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("email", sa.String(255), nullable=True, unique=False),
    sa.Column("name", sa.String(255), nullable=False),
    sa.Column("username", sa.String(255), nullable=False, unique=True),
    sa.Column("password", sa.String(255), nullable=False),
    sa.Column("profile_picture", sa.String(255), nullable=True),
    sa.Column("bio", sa.String(255), nullable=True),
    sa.Column("updated_at", sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now()),
    sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    sa.Column("user_type", sa.Enum(UserType), nullable=False,server_default=UserType.USER.name),
    sa.Column("user_rank", sa.Enum(UserRank), nullable=False, server_default=UserRank.BEGINNER.name),
    sa.Column("is_verified", sa.Boolean, nullable=False, server_default="False"),
)
