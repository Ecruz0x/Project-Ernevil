
from fastapi import FastAPI, Request, HTTPException, status
from .schemas.computer import ComputerWithID, CreateComputer, RefreshComputer
from .schemas.locations import Location
import time, asyncio
from datetime import datetime

app = FastAPI()

computers: list[dict] = []
locations: list[dict] = []

@app.get("/api/computers", response_model = list[ComputerWithID])
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


@app.post("/api/add_computer", response_model = ComputerWithID, status_code = status.HTTP_201_CREATED)
def createComputer(computer: CreateComputer):
    id = len(computers) + 1
    new_computer = {
        "computer_id": id,
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
        "lastHB": datetime.now()
    }
    if new_computer not in computers:
        computers.append(new_computer)
        return  new_computer
    else:
        return False

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