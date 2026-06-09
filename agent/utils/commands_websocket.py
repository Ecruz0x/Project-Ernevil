import asyncio
import websockets
import subprocess
import time
from .websockets_init import agentWebsocket
                

async def commands_ws_client(computer_id: int, is_unix: bool):
    uri = f"ws://127.0.0.1:8000/api/ws?computer_id={computer_id}"
    ws = agentWebsocket(computer_id, is_unix, uri)
    await ws.initializeSocket()
    try:
        await ws.receiveCommands()
    except KeyboardInterrupt:
        exit(1)

def launchCmdWS(computer_id: int, is_unix: bool):
    asyncio.run(commands_ws_client(computer_id, is_unix))