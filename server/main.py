
from fastapi import FastAPI, Request, HTTPException, status, Depends
from sqlalchemy import select, text
from sqlalchemy.orm import Session
from .database import dbschema
from .database.db import Base, engine, get_db
from typing import Annotated

from .routers import add_resources, update_resources, get_resources, delete_resources, heartbeats
from .utils.heartbeat_utils import expireHeartBeat

Base.metadata.create_all(bind=engine)

app = FastAPI()



app.include_router(add_resources.router, prefix = "/api/computers", tags = ["Add Resources"])
app.include_router(get_resources.router, prefix = "/api/computers", tags = ["Get Resources"])
app.include_router(update_resources.router, prefix = "/api/computers", tags = ["Update Resources"])
app.include_router(delete_resources.router, prefix = "/api/computers", tags = ["Delete Resources"])
app.include_router(heartbeats.router, prefix = "/api/computers", tags = ["Heartbeat Handler"])






@app.on_event("startup")
async def main():
    asyncio.create_task(expireHeartBeat())