from ..schemas.refresh import RefreshComputerName, RefreshMemoryInfo, RefreshNetworkingInfo, RefreshProcessesInfo, RefreshDisksInfo, CUsersInfo
from ..schemas.authentication import AuthenticateComputer
import time, asyncio, json
from datetime import datetime
from sqlalchemy import select, text
from sqlalchemy.orm import Session
from ..database import dbschema
from ..database.db import Base, engine, get_db
from typing import Annotated
import json
from fastapi import APIRouter, HTTPException, status, Depends

router = APIRouter()




def authenticateComputer(computer_auth: AuthenticateComputer, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(
                text(f"SELECT 1 FROM computerInfo WHERE computer_id = {computer_auth['computer_id']} AND fingerprint = '{computer_auth['fingerprint']}'")
            )
    existing_computer = result.scalars().first()

    if existing_computer:
        return True
    else: 
        return False


@router.put("/name", response_model = bool)

def refreshComputerName(newData: RefreshComputerName, db: Annotated[Session, Depends(get_db)]):
    auth_data = {"computer_id": newData.computer_id, "fingerprint": newData.fingerprint}
    is_auth = authenticateComputer(auth_data, db)
    name = newData.newcomputername
    if is_auth:
        result = db.execute(select(dbschema.ComputerInfo).where(dbschema.ComputerInfo.computer_id == newData.computer_id))
        computer = result.scalars().first()
        computer.computername = newData.newcomputername
        db.commit()
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Authentication Error",
        )

@router.put("/mem", response_model = bool)

def refreshMemoryInfo(newData: RefreshMemoryInfo, db: Annotated[Session, Depends(get_db)]):
    auth_data = {"computer_id": newData.computer_id, "fingerprint": newData.fingerprint}
    is_auth = authenticateComputer(auth_data, db)
    if is_auth:
        result = db.execute(select(dbschema.MemoryInfo).where(dbschema.MemoryInfo.computer_id == newData.computer_id))
        computer = result.scalars().first()
        computer.totalMemory = newData.totalMemory
        computer.available_memory = newData.available_memory
        computer.usage = newData.usage
        db.commit()
        db.refresh(computer)
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Authentication Error",
        )


@router.patch("/net", response_model = bool)
def refreshNetInfo(newData: RefreshNetworkingInfo, db: Annotated[Session, Depends(get_db)]):
    auth_data = {"computer_id": newData.computer_id, "fingerprint": newData.fingerprint}
    is_auth = authenticateComputer(auth_data, db)
    if is_auth:
        result = db.execute(select(dbschema.networkingInfo).where((dbschema.networkingInfo.computer_id == newData.computer_id) 
            & (newData.ifname == dbschema.networkingInfo.ifname)))
        computer = result.scalars().first()
        refresh_data = newData.model_dump(exclude_unset = True)
        if computer:
            for k, v in refresh_data.items():
                setattr(computer, k, v)
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

