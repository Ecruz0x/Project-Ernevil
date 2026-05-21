from fastapi import FastAPI, Request, HTTPException, status, Depends, APIRouter
from ..schemas.computer import ComputerCreated, CreateComputer
from ..schemas.computer import ComputerInfo, SpecificComputerInfo, MemoryInfo, NetworkingInfo, ProcessesInfo, DisksInfo, CUsersInfo
from datetime import datetime
from sqlalchemy import select, text
from sqlalchemy.orm import Session
from ..database import dbschema
from ..database.db import Base, engine, get_db
from typing import Annotated
import time, asyncio, logging


router = APIRouter()

@router.post("", response_model = ComputerCreated, status_code = status.HTTP_201_CREATED)
def addComputer(computer: CreateComputer, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(
                text(f"SELECT 1 FROM computerInfo WHERE fingerprint = '{computer.fingerprint}'")
            )
    existing_computer = result.scalars().first()

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
        ipaddr=computer.ip_addr[netinterface]
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
        username = dbschema.computerUsers(
        computer=newComputer,
        username = user
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
    added_info = {"computer_id": newComputer.computer_id, "computername" : newComputer.computername, "added_on": newComputer.added_on}
    return added_info


@router.get("", response_model = list[ComputerInfo])
def getComputers(db: Annotated[Session, Depends(get_db)]):
    result = db.execute(text("SELECT * FROM computerInfo"))
    computers = result.mappings().all()
    return computers

@router.get("/live", response_model = list[ComputerInfo])
def getLiveComputers(db: Annotated[Session, Depends(get_db)]) -> list[ComputerInfo]:
    result = db.execute(text("SELECT * FROM computerInfo WHERE is_alive"))
    liveComputers = result.mappings().all()
    return liveComputers

@router.get("", response_model = SpecificComputerInfo)
def getComputer(computer_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(text(f"SELECT * FROM computerInfo WHERE computer_id = {computer_id}"))
    print(result)
    targetComputer = result.mappings().all()
    return targetComputer


@router.get("/mem", response_model = MemoryInfo)
def getMemoryInfo(computer_id: int, db: Annotated[Session, Depends(get_db)]) -> MemoryInfo:
    result = db.execute(text(f"SELECT totalMemory, available_memory, usage FROM memoryinfo WHERE computer_id = {computer_id}"))
    targetdetails = result.mappings().all()
    return targetdetails[0]


@router.get("/net", response_model = list[NetworkingInfo])
def getNetInfo(computer_id: int, db: Annotated[Session, Depends(get_db)]) -> list[NetworkingInfo]:
    result = db.execute(text(f"SELECT ifname, ipaddr FROM netinfo WHERE computer_id = {computer_id}"))
    targetdetails = result.mappings().all()
    return targetdetails

@router.get("/ps", response_model = list[ProcessesInfo])
def getProcessInfo(computer_id: int, db: Annotated[Session, Depends(get_db)]) -> list[ProcessesInfo]:
    result = db.execute(text(f"SELECT pid, user, process_name FROM processesinfo WHERE computer_id = {computer_id}"))
    targetdetails = result.mappings().all()
    return targetdetails

@router.get("/hd", response_model = list[DisksInfo])
def getDisksInfo(computer_id: int, db: Annotated[Session, Depends(get_db)]) -> list[DisksInfo]:
    result = db.execute(text(f"SELECT partitionname, mountpoint, fstype FROM disksinfo WHERE computer_id = {computer_id}"))
    targetdetails = result.mappings().all()
    return targetdetails

@router.get("/users", response_model = list[CUsersInfo])
def getComputerUsers(computer_id: int, db: Annotated[Session, Depends(get_db)]) -> list[CUsersInfo]:
    result = db.execute(text(f"SELECT username FROM computerusers WHERE computer_id = {computer_id}"))
    targetdetails = result.mappings().all()
    return targetdetails