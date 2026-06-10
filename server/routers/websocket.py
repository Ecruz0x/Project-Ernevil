from fastapi import APIRouter, WebSocket, HTTPException, status, WebSocketDisconnect
from ..utils import connection_manager
import asyncio
from ..schemas.executors_schemas import CommandRequest, RestartComputer, ShutdownComputer
import math, os, json
from datetime import datetime, timedelta
from tinydb import TinyDB, Query


router = APIRouter()
agent_ws = connection_manager.ConnectionManager()


ndb_path = './database/notifications.json'
os.makedirs(os.path.dirname(ndb_path), exist_ok=True)
db = TinyDB(ndb_path)
UserQuery = Query()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, computer_id: int):
    await agent_ws.connect(websocket, computer_id)
    while True:
        try:
            await asyncio.sleep(float("inf"))
        except KeyboardInterrupt:
            break


@router.post("/commands")
async def execCommands(commandBody: CommandRequest):
    try:
        websocket = agent_ws.active_connections[commandBody.computer_id]
        await agent_ws.send_specific_message(commandBody.command, websocket)
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
        websocket = agent_ws.active_connections[computer.computer_id]
        await agent_ws.send_specific_message("shutdown now", websocket)
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
        websocket = agent_ws.active_connections[computer.computer_id]
        await agent_ws.send_specific_message("sudo reboot", websocket)
        response = await websocket.receive_text()
        return {"result": response}
    except KeyError as e:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="websocket not found",
        )


@router.websocket("/ws/alert")
async def websocket_endpoint(websocket: WebSocket, computer_id: int, status_code=status.HTTP_201_CREATED):
    
    await agent_ws.connect(websocket, computer_id)

    try:
        while True:
            alert = await websocket.receive_text()
            alertd = json.loads(alert)
            expire_time = datetime.now() + timedelta(hours=1)
            alertd["computer_id"] = computer_id
            alertd['expires_at'] = expire_time.isoformat()
            db.insert(alertd)
    except WebSocketDisconnect as e:
        print(e)


@router.get("/get_alerts")
async def getAlerts():
    try:
        now_str = datetime.now().isoformat()
        active_notifications = db.search(lambda doc: doc['expires_at'] > now_str)
        return active_notifications
    except Exception as e:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=e,
        )