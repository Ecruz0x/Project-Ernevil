from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

class ConnectionManager:
    def __init__(self):
        self.command_connections = {}
        self.usb_alert_connections = {}
        self.pending_responses = {}
        self.ids_alert_connections = {}
        self.alert_connections = {}

    async def connect(self, websocket: WebSocket, computer_id: int, wstype: str):
        await websocket.accept()
        if wstype == "cmd_ws":
            self.command_connections[computer_id] = websocket
        elif wstype == "usb_alert_ws":
            self.usb_alert_connections[computer_id] = websocket
        elif wstype == "ids_alert_ws":
            self.ids_alert_connections[computer_id] = websocket

        print(f"CONNECTED: {computer_id}")

    def disconnect(self, computer_id: int, websocket: WebSocket):
        if websocket in self.usb_alert_connections.values():
            del self.usb_alert_connections[computer_id]
        elif websocket in self.command_connections.values():
            del self.command_connections[computer_id]
        elif websocket in self.ids_alert_connections.values():
            del self.ids_alert_connections[computer_id]
        else:
            raise ValueError("Websocket not found error.")

    async def send_specific_message(self, message: str, websocket: WebSocket):
        if websocket in self.ids_alert_connections.values() or websocket in self.command_connections.values() or self.usb_alert_connections.values():
            await websocket.send_text(message)
        else:
            raise ValueError("Websocket not found error.")

    async def recv_text(self, websocket):
        if websocket in self.ids_alert_connections.values() or websocket in self.command_connections.values() or self.usb_alert_connections.values():
            return await websocket.receive_text()
        else:
            raise ValueError("Websocket not found error.")

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)