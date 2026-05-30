from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Depends
from typing import Annotated
from ..schemas.authentication import AuthenticateComputer
from sqlalchemy.orm import Session
from ..database import dbschema
from ..database.db import Base, engine, get_db
from sqlalchemy import select
from .update_resources import authenticateComputer

router = APIRouter()



@router.post("/heartbeat", response_model = bool, status_code = 200)
def handleHeartBeat(computer: AuthenticateComputer, db: Annotated[Session, Depends(get_db)]):
    auth_data = {"computer_id": computer.computer_id, "fingerprint": computer.fingerprint}
    is_auth = authenticateComputer(auth_data, db)
    if is_auth:
        result = db.execute(select(dbschema.ComputerInfo).where(dbschema.ComputerInfo.computer_id == computer.computer_id))
        computer = result.scalars().first()
        computer.last_heartbeat = datetime.now()
        db.commit()
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Authentication Error",
        )

