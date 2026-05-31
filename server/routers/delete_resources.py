from fastapi import Request, HTTPException, status, Depends, APIRouter
from sqlalchemy import select, text, delete
from sqlalchemy.orm import Session
from ..database import dbschema
from ..database.db import Base, engine, get_db
from typing import Annotated 
from ..schemas.remove_rs_schema import AuthenticateComputer, RemoveNetworkingInfo, RemoveDisksInfo, RCUsersInfo


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
        db.execute(delete(dbschema.networkingInfo)
        .where((dbschema.networkingInfo.computer_id == IFInfo.computer_id) & 
        (dbschema.networkingInfo.ifname == IFInfo.ifname)).execution_options(is_delete_using=True, synchronize_session="fetch"))
        db.commit()
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Authentication Error",
        )

@router.delete("/hd", response_model = bool)
def deleteDiskInfo(HDInfo: RemoveDisksInfo, db: Annotated[Session, Depends(get_db)]):
	auth_data = {"computer_id": HDInfo.computer_id, "fingerprint": HDInfo.fingerprint}
	is_auth = authenticateComputer(auth_data, db)
	if is_auth:
	    db.execute(delete(dbschema.disksInfo)
	    .where((dbschema.disksInfo.computer_id == HDInfo.computer_id) & 
	    (dbschema.disksInfo.partitionname == HDInfo.partitionname)).execution_options(is_delete_using=True, synchronize_session="fetch"))
	    db.commit()
	    return True
	else:
	    raise HTTPException(
	    status_code=status.HTTP_400_BAD_REQUEST,
	    detail="Authentication Error",
	    )

@router.delete("/cusers", response_model = bool)
def deleteUserInfo(UserInfo: RCUsersInfo, db: Annotated[Session, Depends(get_db)]):
	auth_data = {"computer_id": UserInfo.computer_id, "fingerprint": UserInfo.fingerprint}
	is_auth = authenticateComputer(auth_data, db)
	if is_auth:
	    db.execute(delete(dbschema.computerUsers)
	    .where((dbschema.computerUsers.computer_id == UserInfo.computer_id) & 
	    (dbschema.computerUsers.username == UserInfo.username)).execution_options(is_delete_using=True, synchronize_session="fetch"))
	    db.commit()
	    return True
	else:
	    raise HTTPException(
	    status_code=status.HTTP_400_BAD_REQUEST,
	    detail="Authentication Error",
		)