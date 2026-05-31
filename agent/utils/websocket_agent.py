import asyncio
import websockets

async def test_client():
    uri = "ws://127.0.0.1:8000/api/ws"
    async with websockets.connect(uri) as ws:
        while True:
            message = await ws.recv()
            print("Server said:", message)