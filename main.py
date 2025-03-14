from fastapi import FastAPI
from routes.route import router
from database_connect import dbs



app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await dbs.connect()

@app.on_event("shutdown")
async def shutdown_event():
    await dbs.disconnect()

app.include_router(router)