from fastapi import FastAPI, Request, HTTPException, status, Depends, APIRouter
from ..schemas.add_rs_schema import ComputerInfo, MemoryInfo, NetworkingInfo, ProcessesInfo, DisksInfo, CUsersInfo, getCPUInfo
from ..schemas.authentication import AuthUpdates
from ..database import dbschema
from ..database.db import Base, engine, get_db
from typing import Annotated
from sqlalchemy import text, select
from sqlalchemy.orm import Session
from ..auth import ValidUser



router = APIRouter()



#### TODO: Authentication Needed Here

#### Key auth
@router.get("/is_added", response_model = bool)
def isAddedComputer(k: AuthUpdates, db: Annotated[Session, Depends(get_db)]):
    existing_computer = (
        db.query(dbschema.ComputerInfo)
        .filter(dbschema.ComputerInfo.computer_id == k.computer_id)
        .first()
    )

    existing_key = (
        db.query(dbschema.Keys)
        .filter(dbschema.Keys.key == k.key)
        .first()
    )
    if existing_computer and existing_computer:
        return True
    else:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Computer unavailable or unauthorized",
        )


@router.get("", response_model = list[ComputerInfo])
def getComputers(db: Annotated[Session, Depends(get_db)], valid_user: ValidUser):
    result = db.execute(text("SELECT * FROM computerInfo"))
    computers = result.mappings().all()
    return computers

@router.get("/live", response_model = list[ComputerInfo])
def getLiveComputers(db: Annotated[Session, Depends(get_db)], valid_user: ValidUser) -> list[ComputerInfo]:
    result = db.execute(text("SELECT * FROM computerInfo WHERE is_alive AND NOT blacklisted"))
    liveComputers = result.mappings().all()
    return liveComputers

@router.get("/blacklisted", response_model = list[ComputerInfo])
def getBSComputers(db: Annotated[Session, Depends(get_db)], valid_user: ValidUser) -> list[ComputerInfo]:
    result = db.execute(text("SELECT * FROM computerInfo WHERE is_alive AND blacklisted"))
    BSComputers = result.mappings().all()
    return BSComputers


@router.get("/location", response_model = list[str])
def getCmpLoc(location_id: int, db: Annotated[Session, Depends(get_db)], valid_user: ValidUser):
    result = db.execute(
        select(dbschema.ComputerInfo.computername).where(
            dbschema.ComputerInfo.location_id == location_id
        )
    )

    computers = result.scalars().all()
    return computers

@router.get("/c", response_model = ComputerInfo)
def getComputer(computer_id: int, db: Annotated[Session, Depends(get_db)], valid_user: ValidUser):
    result = db.execute(text(f"SELECT * FROM computerInfo WHERE computer_id = {computer_id}"))
    targetComputer = result.mappings().all()
    if targetComputer:
        return targetComputer[0]
    else:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Computer is unreachable.",
        )


@router.get("/mem", response_model = MemoryInfo)
def getMemoryInfo(computer_id: int, db: Annotated[Session, Depends(get_db)], valid_user: ValidUser) -> MemoryInfo:
    result = db.execute(text(f"SELECT totalMemory, available_memory, usage FROM memoryinfo WHERE computer_id = {computer_id}"))
    targetdetails = result.mappings().all()
    if targetdetails:
        return targetdetails[0]
    else:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Computer is offline or unreachable.",
        )

@router.get("/cpu", response_model = getCPUInfo)
def getCpuInfo(computer_id: int, db: Annotated[Session, Depends(get_db)], valid_user: ValidUser) -> MemoryInfo:
    result = db.execute(
        select(
            dbschema.CPUInfo.cpu_usage
        ).where(
            dbschema.CPUInfo.computer_id == computer_id
        )
    )
    targetdetails = result.mappings().all()
    if targetdetails:
        return targetdetails[0]
    else:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Computer is offline or unreachable.",
        )

@router.get("/net", response_model = list[NetworkingInfo])
def getNetInfo(computer_id: int, db: Annotated[Session, Depends(get_db)], valid_user: ValidUser) -> list[NetworkingInfo]:
    result = db.execute(text(f"SELECT ifname, ipaddr FROM netinfo WHERE computer_id = {computer_id}"))
    targetdetails = result.mappings().all()
    if targetdetails:
        return targetdetails
    else:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Computer is offline or unreachable.",
        )

@router.get("/ps", response_model = list[ProcessesInfo])
def getProcessInfo(computer_id: int, db: Annotated[Session, Depends(get_db)], valid_user: ValidUser) -> list[ProcessesInfo]:
    result = db.execute(text(f"SELECT pid, username, name FROM processesinfo WHERE computer_id = {computer_id}"))
    targetdetails = result.mappings().all()
    if targetdetails:
        return targetdetails
    else:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Computer is offline or unreachable.",
        )

@router.get("/hd", response_model = list[DisksInfo])
def getDisksInfo(computer_id: int, db: Annotated[Session, Depends(get_db)], valid_user: ValidUser) -> list[DisksInfo]:
    result = db.execute(text(f"SELECT partitionname, mountpoint, fstype FROM disksinfo WHERE computer_id = {computer_id}"))
    targetdetails = result.mappings().all()
    if targetdetails:
        return targetdetails
    else:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Computer unavailable Error",
        )

@router.get("/cusers", response_model = list[CUsersInfo])
def getComputerUsers(computer_id: int, db: Annotated[Session, Depends(get_db)], valid_user: ValidUser) -> list[CUsersInfo]:
    result = db.execute(text(f"SELECT username FROM computerusers WHERE computer_id = {computer_id}"))
    targetdetails = result.mappings().all()
    if targetdetails:
        return targetdetails
    else:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Computer is offline or unreachable.",
        )

@router.get("/expired", response_model = list[ComputerInfo])
def getExpiredComputers(valid_user: ValidUser):
    result = db.execute(select(dbschema.ComputerInfo).where(dbschema.ComputerInfo.is_alive == False))
    expired_computers = result.mappings().all()
    if expired_computers:
        return expired_computers
    else:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        )