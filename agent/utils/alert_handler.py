from .usb_monitor import launchUsbMon
from .websockets_init import agentWebsocket
import asyncio
from .ml_ids.start_ids import alerts


async def send_usb_alerts(computer_id: int, is_unix: bool):
	uri = f"ws://127.0.0.1:8000/api/ws/alert?computer_id={computer_id}&wstype=alert_ws"

	ws = agentWebsocket(computer_id, is_unix, uri)
	await ws.initializeSocket()
	while True:
		async for event_type, device_info in launchUsbMon():
			await ws.send_alert(type = "USB alert", category = "USB device event", manufacturer = device_info['manufacturer'], product = device_info['product'], event = f"USB device {event_type}ed")


async def send_traffic_alerts(computer_id: int, active_int: str, is_unix: bool):
	uri = f"ws://127.0.0.1:8000/api/ws/alert?computer_id={computer_id}"
	try:
		while True:
			details = await alerts.get()
			print(details)
			details = details + {"type": "Network Alert"}
			await websocket.send_json(details)
	except Exception as e:
		ws = agentWebsocket(computer_id, is_unix, uri)
		await ws.initializeSocket()
		while True:
			details = await alerts.get()
			details = details + {"type": "Network Alert"}
			await websocket.send_json(details)


def start_usb_alerts(computer_id: int, is_unix: bool):
	asyncio.run(send_usb_alerts(computer_id, is_unix))

def start_ids(computer_id: int, active_int: str, is_unix: bool):
	asyncio.run(send_traffic_alerts(computer_id, active_int, is_unix))