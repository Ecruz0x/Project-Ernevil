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
async def websocket_endpoint(websocket: WebSocket, computer_id: int, wstype: str):
    
    await agent_ws.connect(websocket, computer_id, wstype)
    while True:
        message = await agent_ws.recv_text(websocket)

        future = agent_ws.pending_responses.get(computer_id)

        if future and not future.done():
            future.set_result(message)



@router.post("/commands")
async def execCommands(commandBody: CommandRequest):
    websocket = agent_ws.command_connections[commandBody.computer_id]
    future = asyncio.Future()
    agent_ws.pending_responses[commandBody.computer_id] = future
#    print(f"Sending command: {commandBody.command}")
    await websocket.send_text(commandBody.command)
#    print("Command sent successfully")
    try:
        result = await asyncio.wait_for(
            future,
            timeout=5
        )

        return {"result": result}

    except asyncio.TimeoutError:
        return {"result": "Execution timed out"}


@router.post("/screenshot")
def captureSc(computer_id: int):
    pass

@router.post("/shutdown")
async def shutDownComputer(computer: ShutdownComputer):
    try:
        info = {"command": "pwd", "computer_id": computer.computer_id}
        response = await execCommands(info)
        return response
    except KeyError as e:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="websocket not found",
        ) 

@router.post("/restart")
async def restartComputer(computer: RestartComputer):
    try:
        websocket = agent_ws.command_connections[computer.computer_id]
        await agent_ws.send_specific_message("sudo reboot", websocket)
        response = await websocket.receive_text()
        return {"result": response}
    except KeyError as e:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="websocket not found",
        )


@router.websocket("/ws/alert")
async def alert_endpoint(websocket: WebSocket, computer_id: int, wstype: str):
    await websocket.accept()


    try:
        while True:
            if wstype == "usb_alert_ws":
                agent_ws.usb_alert_connections[computer_id] = websocket
                wsu = agent_ws.usb_alert_connections[computer_id]
                alert = await wsu.receive_text()
                alertd = json.loads(alert)
                expire_time = datetime.now() + timedelta(hours=1)
                alertd["computer_id"] = computer_id
                alertd['expires_at'] = expire_time.isoformat()
                db.insert(alertd)
            elif wstype == "ids_alert_ws":
                agent_ws.ids_alert_connections[computer_id] = websocket
                wsids = agent_ws.ids_alert_connections[computer_id]
                alert = await wsids.receive_text()
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