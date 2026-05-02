
from fastapi import FastAPI, Request, HTTPException, status
from server.schemas import ComputerWithID, Location, CreateComputer

app = FastAPI()

computers: list[dict] = []
locations: list[dict] = []

@app.get("/api/computers", response_model = list[ComputerWithID])
def getComputers():
    return computers

@app.get("/api/computer/{computer_id}", response_model = ComputerWithID)
def getComputer(computer_id: int):
    return computers[computer_id-1]


@app.get("/api/locations", response_model = list[Location])
def getLocations():
    return locations


@app.post("/api/computers", response_model = ComputerWithID, status_code = status.HTTP_201_CREATED)
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
        "boot_time": computer.boot_time
    }
    computers.append(new_computer)
    return  new_computer

