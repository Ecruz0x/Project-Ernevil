import asyncio
import websockets
import subprocess


async def ws_client(computer_id: int, is_unix: bool):
    uri = f"ws://127.0.0.1:8000/api/ws?computer_id={computer_id}"

    async with websockets.connect(uri) as ws:
        while True:
            msg = await ws.recv()
            if is_unix:
                result = subprocess.run(msg.split(), capture_output=True, text=True)
            else:
                result = subprocess.run(["powershell.exe", "-NoProfile", "-Command", msg], capture_output=True, text=True)

            await ws.send(result.stdout)

def agent_ws(computer_id: int, is_unix: bool):
    asyncio.run(ws_client(computer_id, is_unix))