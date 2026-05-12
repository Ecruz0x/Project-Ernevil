from ..schemas.computer import RefreshComputer
import time, asyncio, json
from datetime import datetime
from sqlalchemy import select, text
from sqlalchemy.orm import Session
from .database import dbschema
from .database.db import Base, engine, get_db
from typing import Annotated
import json


router = APIRouter()

@router.post("", response_model = int, status_code = status.HTTP_201_CREATED)
def refreshComputerInfo(data: RefreshComputer):
    id = data.computer_id
    update_data = data.dict(exclude_unset=True)
    for computer in computers:
        if computer['computer_id'] == id:
            for k, v in update_data.items():
                computer[k] = v
    return id