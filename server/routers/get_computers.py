from .database.db import Base, engine, get_db
from fastapi import FastAPI, Request, HTTPException, status, Depends, APIRouter
from ..schemas import ComputerInfo, SpecificComputerInfo, MemoryInfo, NetworkingInfo, ProcessesInfo, DisksInfo, CUsersInfo

router = APIRouter()


@router.get("", response_model = list[ComputerInfo])
def getComputers(db: Annotated[Session, Depends(get_db)]):
    result = db.execute(text("SELECT * FROM computerInfo"))
    computers = result.mappings().all()
    return computers

@router.get("", response_model = list[ComputerInfo])
def getLiveComputers(db: Annotated[Session, Depends(get_db)]) -> list[]:
    result = db.execute(text("SELECT * FROM computerInfo WHERE is_alive"))
    liveComputers = result.mappings().all()
    return liveComputers

@router.get("/{computerid}", response_model = SpecificComputerInfo)
def getComputer(computer_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(text(f"SELECT * FROM computerInfo WHERE computerid = {computer_id}"))
    targetComputer = result.mappings().all()
    return targetComputer


@router.get("/{computerid}", response_model = MemoryInfo)
def getMemoryInfo(computer_id: int, db: Annotated[Session, Depends(get_db)]) -> MemoryInfo:
    result = db.execute(text(f"SELECT totalMemory, available_memory, usage FROM memoryinfo WHERE computer_id = {computer_id}"))
    targetdetails = result.mappings().all()
    return targetdetails


@router.get("/{computerid}", response_model = list[NetworkingInfo])
def getNetInfo(computer_id: int, db: Annotated[Session, Depends(get_db)]) -> list[NetworkingInfo]:
    result = db.execute(text(f"SELECT ifname, ipaddr FROM netinfo WHERE computer_id = {computer_id}"))
    targetdetails = result.mappings().all()
    return targetdetails

@router.get("/{computerid}", response_model = list[ProcessesInfo])
def getProcessInfo(computer_id: int, db: Annotated[Session, Depends(get_db)]) -> list[ProcessesInfo]:
    result = db.execute(text(f"SELECT pid, user, process_name FROM processesinfo WHERE computer_id = {computer_id}"))
    targetdetails = result.mappings().all()
    return targetdetails

@router.get("/{computerid}", response_model = list[DisksInfo])
def getDisksInfo(computer_id: int, db: Annotated[Session, Depends(get_db)]) -> list[DisksInfo]:
    result = db.execute(text(f"SELECT partitionname, mountpoint, fstype FROM disksinfo WHERE computer_id = {computer_id}"))
    targetdetails = result.mappings().all()
    return targetdetails

@router.get("/{computerid}", response_model = list[CUsersInfo])
def getComputerUsers(computer_id: int, db: Annotated[Session, Depends(get_db)]) -> list[CUsersInfo]:
    result = db.execute(text(f"SELECT username FROM computerusers WHERE computer_id = {computer_id}"))
    targetdetails = result.mappings().all()
    return targetdetails

