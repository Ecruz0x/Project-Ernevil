from .database.db import Base, engine, get_db
from fastapi import FastAPI, Request, HTTPException, status, Depends, APIRouter

router = APIRouter()


@router.get("")
def getComputers(db: Annotated[Session, Depends(get_db)]):
    result = db.execute(text("SELECT * FROM computerInfo"))
    computers = result.mappings().all()
    return computers

@router.get("")
def getLiveComputers(db: Annotated[Session, Depends(get_db)]):
    result = db.execute(text("SELECT * FROM computerInfo WHERE is_alive"))
    liveComputers = result.mappings().all()
    return liveComputers

@router.get("")
def getComputer(computer_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(text(f"SELECT * FROM computerInfo WHERE computerid = {computer_id}"))
    targetComputer = result.mappings().all()
    return targetComputer


@router.get("")
def getMemoryInfo(computer_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(text(f"SELECT totalMemory, available_memory, usage FROM memoryinfo WHERE computer_id = {computer_id}"))
    targetdetails = result.mappings().all()
    return targetdetails


@router.get("")
def getNetInfo(computer_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(text(f"SELECT * FROM netinfo WHERE computer_id = {computer_id}"))
    targetdetails = result.mappings().all()
    return targetdetails

@router.get("")
def getNetInfo(computer_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(text(f"SELECT pid, user, process_name FROM processesinfo WHERE computer_id = {computer_id}"))
    targetdetails = result.mappings().all()
    return targetdetails

@router.get("")
def getDisksInfo(computer_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(text(f"SELECT partitionname, mountpoint, fstype FROM disksinfo WHERE computer_id = {computer_id}"))
    targetdetails = result.mappings().all()
    return targetdetails

@router.get("")
def getComputerUsers(computer_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(text(f"SELECT username FROM computerusers WHERE computer_id = {computer_id}"))
    targetdetails = result.mappings().all()
    return targetdetails