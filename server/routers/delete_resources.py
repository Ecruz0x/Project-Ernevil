from fastapi import FastAPI, Request, HTTPException, status, Depends, APIRouter
from sqlalchemy import select, text
from sqlalchemy.orm import Session
from ..database import dbschema
from ..database.db import Base, engine, get_db
from typing import Annotated


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


@router.delete("/net", response_model = bool)
def deleteNetInfo(IFInfo: RemoveNetworkingInfo, db: Annotated[Session, Depends(get_db)]):
    auth_data = {"computer_id": IFInfo.computer_id, "fingerprint": IFInfo.fingerprint}
    is_auth = authenticateComputer(auth_data, db)
    if is_auth:
        db.execute(delete(dbschema.networkingInfo).where((dbschema.networkingInfo.computer_id == IFInfo.computer_id) & (dbschema.networkingInfo.ifname == IFInfo.ifname)))
        db.commit()
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Authentication Error",
        )