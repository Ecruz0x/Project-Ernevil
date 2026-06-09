from .usb_monitor import launchUsbMon
from .websockets_init import agentWebsocket
import asyncio


async def send_usb_alerts(computer_id: int, is_unix: bool):
	uri = f"ws://127.0.0.1:8000/api/ws/alert?computer_id={computer_id}"

	ws = agentWebsocket(computer_id, is_unix, uri)
	await ws.initializeSocket()
	while True:
		async for event_type, device_info in launchUsbMon():
			await ws.send_alert(type = "alert", category = "USB device event", manufacturer = device_info['manufacturer'], product = device_info['product'], message = f"USB device {event_type}ed")



def start_usb_alerts(computer_id: int, is_unix: bool):
	asyncio.run(send_usb_alerts(computer_id, is_unix))

