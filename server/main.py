
from fastapi import FastAPI, Request, HTTPException, status, Depends
from .schemas.computer import ComputerWithID, CreateComputer, RefreshComputer
from .schemas.locations import Location, CreateLocation, RLocation
import time, asyncio
from datetime import datetime
from sqlalchemy import select, text
from sqlalchemy.orm import Session
from .database import dbschema
from .database.db import Base, engine, get_db
from typing import Annotated

Base.metadata.create_all(bind=engine)

app = FastAPI()




"""


@app.get("/api/locations", response_model = list[Location])
def getLocations():
    return locations





@app.post("/api/refresh", response_model = int, status_code = status.HTTP_201_CREATED)
def refreshComputer(data: RefreshComputer):
    id = data.computer_id
    update_data = data.dict(exclude_unset=True)
    for computer in computers:
        if computer['computer_id'] == id:
            for k, v in update_data.items():
                computer[k] = v
    return id


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