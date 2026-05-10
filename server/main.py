
from fastapi import FastAPI, Request, HTTPException, status, Depends
from .schemas.computer import ComputerWithID, CreateComputer, RefreshComputer
from .schemas.locations import Location, CreateLocation, RLocation
import time, asyncio, json
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import Session
from .database import dbschema
from .database.db import Base, engine, get_db
from typing import Annotated

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/api/add_computer", response_model = bool, status_code = status.HTTP_201_CREATED)
def createComputer(computer: CreateComputer, db: Annotated[Session, Depends(get_db)]):
    """result = db.execute(
                    select(dbschema.ComputerInfo).where(dbschema.ComputerInfo.fingerprint == "computer.fingerprint")
                )"""
    existing_computer = False              

##ADD CPU COUNT
    if existing_computer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Computer already exists",
        )

    newComputer = dbschema.ComputerInfo(
        computername=computer.computer_name,
        is_unix=computer.is_unix,
        boottime=computer.boot_time,
        is_alive=True,
        node_machineid=computer.node_machineid,
        fingerprint= computer.fingerprint,
        uuid= computer.uuid,
        added_on=datetime.now(),
        os=computer.os,
        )
    MemInfo = dbschema.MemoryInfo(
        computer=newComputer,
        totalMemory = computer.memory['totalMemory'],
        available_memory = computer.memory['availableMemory'],
        usage=computer.memory['usage']
        )
    interfaces = []
    for netinterface in computer.ip_addr.keys():
        interface = dbschema.networkingInfo(
        computer=newComputer,
        ifname=netinterface,
        ipaddr=computer.ip_addr[netinterface][0]
        )
        interfaces.append(interface)
    processes = []
    for process in computer.processes:
        processesInfo = dbschema.processesInfo(
        computer=newComputer,
        pid=process['pid'],
        user=process['username'],
        process_name=process['name']
        )
        processes.append(processesInfo)

    users = []
    for user in computer.users:
        username = dbschema.processesInfo(
        computer=newComputer,
        user = user
        )
        users.append(username)

    disks = []
    for disk in computer.disks.values():
        disksInfo = dbschema.disksInfo(
            computer=newComputer,
            partitionname=disk['device'],
            mountpoint=disk['mountpoint'],
            fstype=disk['fstype']
        )
        disks.append(disksInfo)
    db.add_all([newComputer, MemInfo])
    db.add_all(interfaces)
    db.add_all(processes)
    db.add_all(disks)
    db.add_all(users)
    db.commit()
    return True
"""
@app.get("/api/computers", response_model = list[ComputerWithID])
def getComputers():
    return computers

@app.get("/api/livecomputers", response_model = list[ComputerWithID])
def getLiveComputers():
    liveComputers = []
    for computer in computers:
        if computer["is_alive"]:
            liveComputers.append(computer)
    return liveComputers



@app.get("/api/computer/{computer_id}", response_model = ComputerWithID)
def getComputer(computer_id: int):
    return computers[computer_id-1]


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