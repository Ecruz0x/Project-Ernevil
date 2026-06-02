import asyncio
import websockets

async def test_client(computer_id: int):
    uri = f"ws://127.0.0.1:8000/api/ws?computer_id={computer_id}"
    async with websockets.connect(uri) as ws:
        while True:
            message = input("Mess: ")
            await ws.send(message)
            response = await ws.recv()
            print(response)


asyncio.run(test_client(1))