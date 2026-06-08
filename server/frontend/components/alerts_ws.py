from websocket_init import frontendWebsocket
import asyncio


async def alertsWS(computer_id):
	uri = f"ws://127.0.0.1:8000/api/ws/alert?computer_id={computer_id}"
	ws = frontendWebsocket(computer_id, uri)
	await ws.initializeSocket()
	alert = await ws.receiveAlerts()
	while alert:
		print(alert)


asyncio.run(alertsWS(9619))
