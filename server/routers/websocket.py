from fastapi import APIRouter, WebSocket
from ..utils import connection_manager


router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, computer_id: int):
    manager = connection_manager.ConnectionManager()
    await manager.connect(websocket, computer_id)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_specific_message(f"You wrote: {data}", manager.active_connections[computer_id])
    except Exception as e:
        pass
