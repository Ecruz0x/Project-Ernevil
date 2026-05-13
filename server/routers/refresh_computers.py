from ..schemas.computer import RefreshComputerName, RefreshMemoryInfo, RefreshNetworkingInfo, RefreshProcessesInfo, RefreshDisksInfo, CUsersInfo
from ..schemas.autentication import AuthenticateComputer
import time, asyncio, json
from datetime import datetime
from sqlalchemy import select, text
from sqlalchemy.orm import Session
from .database import dbschema
from .database.db import Base, engine, get_db
from typing import Annotated
import json


router = APIRouter()


def authenticateComputer(computer_auth: AuthenticateComputer):
    result = db.execute(
                text(f"SELECT 1 FROM computerInfo WHERE computerid = {computer_auth.computer_id} AND fingerprint = '{computer_auth.fingerprint}'")
            )
    existing_computer = result.scalars().first()

    if existing_computer:
        return True
    else: 
        return False


def refreshComputerName(newData: RefreshComputerName):
    is_auth = authenticateComputer(newData.computer_id, newData.fingerprint)
    name = newData.newcomputername
    if is_auth:
        result = db.execute(
                text(f"UPDATE computerInfo SET computername = '{name}' WHERE computerid = {newData.computer_id}")
            )
    else:
        raise Exception(AuthenticationError)

def refreshMemoryInfo(newData: RefreshMemoryInfo):
    is_auth = authenticateComputer(newData.computer_id, newData.fingerprint)
    if is_auth:
        result = db.execute(
                text(f"UPDATE memoryinfo SET totalMemory = {newData.totalMemory}, available_memory = {newData.available_memory}, usage = {newData.usage} WHERE computerid = {newData.computer_id}")
            )
    else:
        raise Exception(AuthenticationError)


def refreshNetworkingInfo(newData: list[RefreshNetworkingInfo]):
    is_auth = authenticateComputer(newData.computer_id, newData.fingerprint)
    if is_auth:
        result = db.execute(
                text(f"UPDATE netinfo SET available_memory = {newData.available_memory}, usage = {newData.usage} WHERE computerid = {newData.computer_id}")
            )
    else:
        raise Exception(AuthenticationError)


d