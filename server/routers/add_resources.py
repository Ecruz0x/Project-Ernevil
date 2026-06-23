from fastapi import FastAPI, Request, HTTPException, status, Depends, APIRouter
from ..schemas.add_rs_schema import ComputerCreated, CreateComputer, addKey
from ..schemas.add_rs_schema import ComputerInfo, MemoryInfo, NetworkingInfo, ProcessesInfo, DisksInfo, CUsersInfo, usbInfo
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
        select(dbschema.ComputerInfo).where(
            dbschema.ComputerInfo.fingerprint == computer.fingerprint
        )
    )
    existing_computer = result.scalars().first()
    existing_key = (
        db.query(dbschema.Keys)
        .filter(dbschema.Keys.key == computer.key)
        .first()
    )

##ADD CPU COUNT
    if existing_computer or not existing_key:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Adding error, please check your key and try again",
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
        blacklisted = False
        )
    MemInfo = dbschema.MemoryInfo(
        computer=newComputer,
        totalMemory = computer.memory['totalMemory'],
        available_memory = computer.memory['availableMemory'],
        usage=computer.memory['usage']
        )
    CpuInfo = dbschema.CPUInfo(
        computer = newComputer,
        cpu_usage = computer.cpu_usage
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
        username=process['username'],
        name=process['name']
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
    for k, v in computer.disks.items():
        disksInfo = dbschema.disksInfo(
            computer = newComputer,
            partitionname = k,
            mountpoint = v['mountpoint'],
            fstype = v['fstype']
        )
        disks.append(disksInfo)
    usbDev = []
    for dev in computer.usb_devices:
        deviceInfo = dbschema.usbInfo(
                computer = newComputer,
                manufacturer = dev["manufacturer"],
                product = dev["product"],
                vendor_id = dev["vendor_id"],
                product_id = dev["product_id"]
            )
        usbDev.append(deviceInfo)
    db.add_all([newComputer, MemInfo])
    db.add_all(interfaces)
    db.add_all(processes)
    db.add_all(disks)
    db.add_all(users)
    db.add_all(usbDev)
    db.commit()
    added_info = {"computer_id": newComputer.computer_id, "computername" : newComputer.computername, "added_on": datetime.now()}
    return added_info

@router.post("/keys", response_model = bool, status_code = status.HTTP_201_CREATED)
def addKey(key: addKey, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(
                text(f"SELECT 1 FROM keys WHERE key = '{key.key}'")
            )
    existing_key = result.scalars().first()
    if existing_key:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="key already exists",
        )
    
    newKey = dbschema.Keys(
        key = key.key,
        length = key.length
    )

    db.add(newKey)
    db.commit()
    return True


