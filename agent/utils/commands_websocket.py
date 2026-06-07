import asyncio
import websockets
import subprocess
import time
from websockets_init import agentWebsocket
                

def commands_ws_client(computer_id: int, is_unix: bool):
    uri = f"ws://127.0.0.1:8000/api/ws?computer_id={computer_id}"
    ws = agentWebsocket(computer_id, is_unix, uri)
    asyncio.run(ws.initializeSocket())
    asyncio.run(ws.receiveCommands())