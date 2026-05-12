
from fastapi import FastAPI, Request, HTTPException, status, Depends
from sqlalchemy import select, text
from sqlalchemy.orm import Session
from .database import dbschema
from .database.db import Base, engine, get_db
from typing import Annotated

from .routers import computers

Base.metadata.create_all(bind=engine)

app = FastAPI()



app.include_router(computers.router, prefix = "/api/computers", tags = ["computers"])




"""








@app.post("/api/heartbeat", response_model = bool, status_code = 200)
def handleHeartBeat(computer_id: dict):
    for k in computers:
        if k["computer_id"] == computer_id["id"]:
            k["lastHB"] = datetime.now()
            k["is_alive"] = True
            return True
        else:
            return False


@app.get("/api/expired")
def expiredComputers():
    expired_computers = {}
    for k in computers:
        if k["is_alive"] == False:
            expired_computers[k["computer_id"]] = k["lastHB"]
    return expired_computers


async def expireHeartBeat():
    while True:
        for k in computers:
            duration = datetime.now() - k["lastHB"]
            if duration.total_seconds() >= 150:
                k["is_alive"] = False
        await asyncio.sleep(50)

@app.on_event("startup")
async def startExpiringHBs():
    asyncio.create_task(expireHeartBeat())"""