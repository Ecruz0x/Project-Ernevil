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


@router.post("/name", response_model = bool)

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

@router.post("/mem", response_model = bool)

def refreshMemoryInfo(newData: RefreshMemoryInfo, db: Annotated[Session, Depends(get_db)]):
    auth_data = {"computer_id": newData.computer_id, "fingerprint": newData.fingerprint}
    is_auth = authenticateComputer(auth_data, db)
    if is_auth:
        result = db.execute(select(dbschema.MemoryInfo).where(dbschema.MemoryInfo.computer_id == newData.computer_id))
        computer = result.scalars().first()
        computer.memoryinfo = newData.totalMemory
        computer.available_memory = newData.available_memory
        computer.usage = newData.usage
        db.commit()
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Authentication Error",
        )


@router.post("/net", response_model = bool)

def refreshNetInfo(newData: RefreshMemoryInfo, db: Annotated[Session, Depends(get_db)]):
    auth_data = {"computer_id": newData.computer_id, "fingerprint": newData.fingerprint}
    is_auth = authenticateComputer(auth_data, db)
    if is_auth:
        result = db.execute(
                text(f"UPDATE memoryinfo SET totalMemory = {newData.totalMemory}, available_memory = {newData.available_memory}, usage = {newData.usage} WHERE computer_id = {newData.computer_id}")
            )
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Authentication Error",
        )

