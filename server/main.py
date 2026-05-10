
from fastapi import FastAPI, Request, HTTPException, status, Depends
from .schemas.computer import ComputerWithID, CreateComputer, RefreshComputer
from .schemas.locations import Location, CreateLocation, RLocation
import time, asyncio, json
from datetime import datetime
from .utils import fingerprint as fp
from sqlalchemy import select
from sqlalchemy.orm import Session
import dbschema
from db import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/api/add_computer", response_model = bool, status_code = status.HTTP_201_CREATED)
def createComputer(computer: CreateComputer, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(
        select(models.ComputerInfo).where(models.ComputerInfo.fingerprint == computer.fingerprint),
    )
    existing_computer = result.scalars().first()
    new_computer = {
        "computer_id": computer.computer_id,
        "fingerprint": fp.fingerprint(computer.computer_id, computer.node_machineid),
        "is_unix": computer.is_unix,
        "computer_name": computer.computer_name,
        "location": computer.location,
        "users_count": computer.users_count,
        "users": computer.users,
        "cpu_count": computer.cpu_count,
        "cpu_usage": computer.cpu_usage,
        "memory": computer.memory,
        "disk_count": computer.disk_count,
        "disks": computer.disks,
        "ifcount": computer.ifcount,
        "ip_addr": computer.ip_addr,
        "processes_count": computer.processes_count,
        "processes": computer.processes,
        "boot_time": computer.boot_time,
        "is_alive": True,
        "lastHB": str(datetime.now()),
        "node_machineid": computer.node_machineid
    }


    newComputer = dbschema.ComputerInfo(
        computername=computer.computer_name,
        is_unix=computer.is_unix,
        boottime=computer.boot_time,
        is_alive=True,
        node_machineid=computer.node_machineid,
        fingerprint= fp.fingerprint(computer.uuid, computer.node_machineid),
        uuid= computer.uuid
    )
    computerMemInfo = dbschema.MemoryInfo(
        computer=new_computer,
        totalMemory = computer.memory['totalMemory'],
        available_memory = computer.memory['availableMemory'],
        usage=computer.memory['usage']
    )

    networkingInfo = dbschema.networkingInfo(
        computer=new_computer,
        ifname=computer.ip_addr.keys(),
        ipaddr=computer.ip_addr.values()[0]
    )
    
    for process in computer.processes:
        processesInfo = dbschema.processesInfo(
        computer=new_computer,
        pid=process['pid'],
        user=process['username'],
        process_name=process['name']
    )

    disksInfo = dbschema.disksInfo(
        computer=new_computer,
        for 
    )
    return new_computer.id

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
    asyncio.create_task(expireHeartBeat())