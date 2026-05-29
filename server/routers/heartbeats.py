from datetime import datetime
from fastapi import FastAPI, APIRouter
from ..schemas.authentication import AuthenticateComputer


router = APIRouter()



@router.post("/heartbeat", response_model = bool, status_code = 200)
def handleHeartBeat(computer: AuthenticateComputer):
	
    for k in computers:
        if k["computer_id"] == computer_id["id"]:
            k["lastHB"] = datetime.now()
            k["is_alive"] = True
            return True
        else:
            return False