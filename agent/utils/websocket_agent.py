import asyncio
import websockets
import subprocess
import time


async def ws_client(computer_id: int, is_unix: bool):
    uri = f"ws://127.0.0.1:8000/api/ws?computer_id={computer_id}"
    max_retries = 5
    curr_retries = 0
    while curr_retries < max_retries:
        try:
            async with websockets.connect(uri) as ws:
                while True:
                    print("Websocket established!")
                    msg = await ws.recv()
                    if is_unix:
                        result = subprocess.run(msg.split(), capture_output=True, text=True)
                    else:
                        if msg == "shutdown now":
                            msg = "Stop-Computer -Force"
                        elif msg == "sudo reboot":
                            msg = "Restart-Computer -Force"
                            
                        result = subprocess.run(["powershell.exe", "-NoProfile", "-Command", msg], capture_output=True, text=True)
                    if result.stdout:
                        await ws.send(result.stdout)
                    elif result.stderr:
                        await ws.send(result.stderr)
                    else:
                        status_code = result.returncode
                        if status_code == 0:
                            await ws.send("Command Executed!")
                        else:
                            await ws.send("Command Failed!")
        except Exception as e:
            curr_retries += 1
            print("Websockets Error, Retrying connection...")
    print("Could not establish websockets communication.")
                

def agent_ws(computer_id: int, is_unix: bool):
    asyncio.run(ws_client(computer_id, is_unix))