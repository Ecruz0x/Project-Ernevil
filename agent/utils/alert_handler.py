from usb_monitor import startUSBMonitoring
from websockets_init import agentWebsocket
import asyncio


async def alert_ws_client(computer_id: int, is_unix: bool):
	uri = f"ws://127.0.0.1:8000/api/ws/alert?computer_id={computer_id}"

	ws = agentWebsocket(computer_id, is_unix, uri)
	await ws.initializeSocket()

	for event_type, device_info in startUSBMonitoring():
		await ws.send_alert(
			f"USB device {event_type}ed - "
			f"manufacturer: {device_info['manufacturer']}, "
			f"product: {device_info['product']}"
		)

asyncio.run(alert_ws_client(1, False))

