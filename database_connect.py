import databases as dbs
import sqlalchemy as sa
import os
import redis


POSTGRES_USER = os.environ.get("username", "postgres")
POSTGRES_PASSWORD = os.environ.get("password", "123")
POSTGRES_DB = os.environ.get("database", "ov")
POSTGRES_HOST = os.environ.get("hostname", "localhost")
POSTGRES_PORT = os.environ.get("port", "5432")
REDIS_URL = os.environ.get("redis_url", "5432")

PRODUCTION_ENV = True 
if PRODUCTION_ENV:
    DATABASE_URL = (
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
        f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )
else:
    DATABASE_URL = "postgresql://onevibeuser:S7AvEcHFdcTtOV3zcUhTrMCYagD0B8RZ@dpg-cvbchp5umphs73anapug-a.singapore-postgres.render.com/ovdb"
print("Connection URL:", DATABASE_URL)

try:
    dbs = dbs.Database(DATABASE_URL)
    metadata = sa.MetaData()
except Exception as e:
    print(f"Error connecting to database: {e}")

## Redis
redis_client = redis.Redis(REDIS_URL,decode_responses=True)
