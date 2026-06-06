from fastapi import APIRouter, WebSocket, HTTPException, status
from ..utils import connection_manager
import asyncio
from ..schemas.executors_schemas import CommandRequest, RestartComputer, ShutdownComputer


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
async def shutDownComputer(computer: ShutdownComputer):
    try:
        websocket = manager.active_connections[computer.computer_id]
        await manager.send_specific_message("shutdown now", websocket)
        response = await websocket.receive_text()
        return {"result": response}
    except KeyError as e:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="websocket not found",
        ) 

@router.post("/restart")
async def restartComputer(computer: RestartComputer):
    try:
        websocket = manager.active_connections[computer.computer_id]
        await manager.send_specific_message("sudo reboot", websocket)
        response = await websocket.receive_text()
        return {"result": response}
    except KeyError as e:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="websocket not found",
        )


