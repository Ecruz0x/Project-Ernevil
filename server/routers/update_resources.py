from ..schemas.update_rs_schema import UpdateComputerName, UpdateMemoryInfo, UpdateNetworkingInfo, UpdateProcessesInfo, UpdateDisksInfo, UCUsersInfo, UpdateBootTime
from ..schemas.authentication import AuthenticateComputer
import time, asyncio, json
from datetime import datetime
from sqlalchemy import select, text, delete
from sqlalchemy.orm import Session
from ..database import dbschema
from ..database.db import Base, engine, get_db
from typing import Annotated
import json
from fastapi import APIRouter, HTTPException, status, Depends

router = APIRouter()




def authenticateComputer(computer_auth, db):
    result = db.execute(
        select(dbschema.ComputerInfo).where(
            dbschema.ComputerInfo.computer_id == computer_auth["computer_id"],
            dbschema.ComputerInfo.fingerprint == computer_auth["fingerprint"]
        )
    )

    existing_computer = result.scalars().first()

    if existing_computer:
        return True
    else: 
        return False


@router.put("/name", response_model = bool)
def updateComputerName(newName: UpdateComputerName, db: Annotated[Session, Depends(get_db)]):
    auth_data = {"computer_id": newName.computer_id, "fingerprint": newName.fingerprint}
    is_auth = authenticateComputer(auth_data, db)
    if is_auth:
        result = db.execute(select(dbschema.ComputerInfo).where(dbschema.ComputerInfo.computer_id == newName.computer_id))
        computer = result.scalars().first()
        computer.computername = newName.newcomputername
        db.commit()
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Authentication Error",
        )

@router.put("/mem", response_model = bool)
def updateMemoryInfo(newMemInfo: UpdateMemoryInfo, db: Annotated[Session, Depends(get_db)]):
    auth_data = {"computer_id": newMemInfo.computer_id, "fingerprint": newMemInfo.fingerprint}
    is_auth = authenticateComputer(auth_data, db)
    if is_auth:
        result = db.execute(select(dbschema.MemoryInfo).where(dbschema.MemoryInfo.computer_id == newMemInfo.computer_id))
        computer = result.scalars().first()
        if computer:
            computer.totalMemory = newMemInfo.totalMemory
            computer.available_memory = newMemInfo.available_memory
            computer.usage = newMemInfo.usage
        db.commit()
        db.refresh(computer)
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Authentication Error",
        )


@router.patch("/net", response_model = bool)
def updateNetInfo(newNetInfo: UpdateNetworkingInfo, db: Annotated[Session, Depends(get_db)]):
    auth_data = {"computer_id": newNetInfo.computer_id, "fingerprint": newNetInfo.fingerprint}
    is_auth = authenticateComputer(auth_data, db)
    if is_auth:
        result = db.execute(select(dbschema.networkingInfo).where((dbschema.networkingInfo.computer_id == newNetInfo.computer_id) 
            & (newNetInfo.ifname == dbschema.networkingInfo.ifname)))
        computer = result.scalars().first()
        refresh_data = newNetInfo.model_dump(exclude_unset = True)
        if computer:
            computer.ifname = newNetInfo.ifname
            computer.ipaddr = newNetInfo.ipaddr
        else:
            to_add = refresh_data
            to_add.pop("fingerprint")
            computer = dbschema.networkingInfo(**to_add)
            db.add(computer)

        db.commit()
        db.refresh(computer)
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Authentication Error",
        )

@router.put("/ps", response_model = bool)
def updateProcessesInfo(newPsInfo: list[UpdateProcessesInfo], db: Annotated[Session, Depends(get_db)]):
    auth_data = {"computer_id": newPsInfo[0].computer_id, "fingerprint": newPsInfo[0].fingerprint}
    is_auth = authenticateComputer(auth_data, db)
    if is_auth:
        db.execute(delete(dbschema.processesInfo).where(dbschema.processesInfo.computer_id == newPsInfo[0].computer_id))
        for process in newPsInfo:
            to_add = process.model_dump(exclude_unset = True)
            to_add.pop("fingerprint")
            psinf = dbschema.processesInfo(**to_add)
            db.add(psinf)
        db.commit()
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Authentication Error",
        )



## Needs DELETE endpoint
@router.patch("/hd", response_model = bool)
def updateDisksInfo(newHdInfo: UpdateDisksInfo, db: Annotated[Session, Depends(get_db)]):
    auth_data = {"computer_id": newHdInfo.computer_id, "fingerprint": newHdInfo.fingerprint}
    is_auth = authenticateComputer(auth_data, db)
    if is_auth:
        refresh_data = newHdInfo.model_dump(exclude_unset = True)
        to_add = refresh_data
        to_add.pop("fingerprint")
        computer = dbschema.disksInfo(**to_add)
        db.add(computer)
        db.commit()
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Authentication Error",
        )


## Needs DELETE endpoint
@router.patch("/cusers", response_model = bool)
def updateUserInfo(newUserInfo: UCUsersInfo, db: Annotated[Session, Depends(get_db)]):
    auth_data = {"computer_id": newUserInfo.computer_id, "fingerprint": newUserInfo.fingerprint}
    is_auth = authenticateComputer(auth_data, db)
    if is_auth:
        refresh_data = newUserInfo.model_dump(exclude_unset = True)
        to_add = refresh_data
        to_add.pop("fingerprint")
        computer = dbschema.computerUsers(**to_add)
        db.add(computer)
        db.commit()
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Authentication Error",
        )

@router.patch("/bt", response_model = bool)
def updateBootTime(boottime: UpdateBootTime, db: Annotated[Session, Depends(get_db)]):
    auth_data = {"computer_id": boottime.computer_id, "fingerprint": boottime.fingerprint}
    is_auth = authenticateComputer(auth_data, db)
    if is_auth:
        result = db.execute(select(dbschema.ComputerInfo).where(dbschema.ComputerInfo.computer_id == boottime.computer_id))
        computer = result.scalars().first()
        if computer:
            computer.boottime = boottime.boottime
        db.commit()
        db.refresh(computer)
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Authentication Error",
        )
