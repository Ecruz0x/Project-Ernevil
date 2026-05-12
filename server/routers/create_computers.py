from ..schemas.computer import ComputerCreated, CreateComputer
from datetime import datetime
from sqlalchemy import select, text
from sqlalchemy.orm import Session
from ..database import dbschema
from ..database.db import Base, engine, get_db
from typing import Annotated
import time, asyncio
from fastapi import FastAPI, Request, HTTPException, status, Depends, APIRouter
import models

router = APIRouter()

@router.post("", response_model = ComputerCreated, status_code = status.HTTP_201_CREATED)
def createComputer(computer: CreateComputer, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(
                text(f"SELECT 1 FROM computerInfo WHERE fingerprint = '{computer.fingerprint}'")
            )
    existing_computer = result.scalars().first()
    print(existing_computer)

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
    success = ComputerCreated(newComputer.computerid, newComputer.computername, added_on)