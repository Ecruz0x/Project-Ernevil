from fastapi import APIRouter, WebSocket, HTTPException, status
from ..utils import connection_manager
import asyncio
from ..schemas.executors_schemas import CommandRequest


router = APIRouter()
manager = connection_manager.ConnectionManager()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, computer_id: int):
    await manager.connect(websocket, computer_id)
    while True:
        await asyncio.sleep(60)


@router.post("/commands")
async def execCommands(commandBody: CommandRequest):
    try:
        websocket = manager.active_connections[commandBody.computer_id]
        await manager.send_specific_message(commandBody.command, websocket)
        response = await websocket.receive_text()
        print(response)
        return {"result": response}
    except KeyError as e:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="websocket not found",
        ) 

@router.post("/screenshot")
def captureSc(computer_id: int):
    pass

@router.post("/shutdown")
def shutDownComputer(computer_id: int):
    pass

@router.post("/restart")
def restartComputer(computer_id: int):
    pass
