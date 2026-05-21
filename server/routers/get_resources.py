from fastapi import FastAPI, Request, HTTPException, status, Depends, APIRouter
from ..schemas.add_rs_schema import ComputerInfo, SpecificComputerInfo, MemoryInfo, NetworkingInfo, ProcessesInfo, DisksInfo, CUsersInfo
from ..database import dbschema
from ..database.db import Base, engine, get_db
from typing import Annotated
from sqlalchemy import text
from sqlalchemy.orm import Session

router = APIRouter()



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