from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict = {}

    async def connect(self, websocket: WebSocket, computer_id: int):
        await websocket.accept()
        self.active_connections[computer_id] = websocket

    def disconnect(self, computer_id: int):
        if websocket in self.active_connections.values():
            del self.active_connections[computer_id]
        else:
            raise ValueError("Websocket not found error.")

    async def send_specific_message(self, message: str, websocket: WebSocket):
        if websocket in self.active_connections.values():
            await websocket.send_text(message)
        else:
            raise ValueError("Websocket not found error.")

    async def recv_text(self, websocket):
        if websocket in self.active_connections.values():
            return await websocket.receive_text()
        else:
            raise ValueError("Websocket not found error.")

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)