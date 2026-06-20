import asyncio
import websockets
import subprocess
import time
import json
from .websockets_init import agentWebsocket
                


with open("serverdata.json", "r") as data:
    server_data = json.load(data)

async def commands_ws_client(computer_id: int, is_unix: bool):
    uri = f"wss://{server_data['server_ip']}:{server_data['server_port']}/api/ws?computer_id={computer_id}&wstype=cmd_ws"
    agentws = agentWebsocket(computer_id, is_unix, uri)
    await agentws.initializeSocket(server_data["cert"])
    if agentws.ws is None:
        print("Failed to establish websocket")
        return
    await agentws.receiveCommands()
def launchCmdWS(computer_id: int, is_unix: bool):
    asyncio.run(commands_ws_client(computer_id, is_unix))
    