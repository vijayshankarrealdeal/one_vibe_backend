from database_connect import dbs
from db.db_user_table import db_user_table


async def get_user(id: int):
    query  = db_user_table.select().where(db_user_table.c.id == id)
    user_data = await dbs.fetch_one(query)
    return user_data