from .usb_monitor import launchUsbMon
from .websockets_init import agentWebsocket
import asyncio, time, joblib, warnings
from .ml_ids.netsniffer import capture_and_flow_control as capture
from multiprocessing import Queue
from collections import Counter
from datetime import datetime
from threading import Lock
from threading import Thread
import json


warnings.filterwarnings("ignore", category=UserWarning)


model = joblib.load("utils/ml_ids/models/bestmodel.pkl")

with open("serverdata.json", "r") as data:
    server_data = json.load(data)


now = datetime.now()
sql_format = now.strftime('%Y-%m-%d %H:%M:%S')


model_lock = Lock()
alert_queue = Queue()


def flow_verify(details):
	try:
		prediction = model.predict([details])
		if prediction[0] != "Benign" and prediction[0] != "Botnet_ARES":
			alert_queue.put({
				"src_port": details[0],
				"protocol": "TCP" if details[2] == 0 else "UDP",
				"event": prediction[0]
            })
  

	except Exception as e:
		import traceback
		traceback.print_exc()
		print("MODEL ERROR:", repr(e))



async def send_usb_alerts(computer_id: int, is_unix: bool, cert: str):
	uri = f"wss://{server_data['server_ip']}:{server_data['server_port']}/api/ws/alert?computer_id={computer_id}&wstype=usb_alert_ws"

	ws = agentWebsocket(computer_id, is_unix, uri)
	await ws.initializeSocket(cert)
	while True:
		async for event_type, device_info in launchUsbMon():
			await ws.send_alert(type = "USB alert", category = "USB device event", manufacturer = device_info['manufacturer'], product = device_info['product'], event = f"USB device {event_type}ed")


async def send_traffic_alerts(computer_id: int, active_int: str, is_unix: bool, cert: str):
	uri = f"wss://{server_data['server_ip']}:{server_data['server_port']}/api/ws/alert?computer_id={computer_id}&wstype=ids_alert_ws"
	Thread(
        target=capture,
        args=(active_int, flow_verify),
        daemon=True
    ).start()
	print("Started AI-Based IDS...")
	ws = agentWebsocket(computer_id, is_unix, uri)
	await ws.initializeSocket(cert)
	while True:
		alert = await asyncio.to_thread(alert_queue.get)
		alert["type"] = "Network Alert"
		await ws.send_alert(**alert)


def start_usb_alerts(computer_id: int, is_unix: bool, cert: str):
	asyncio.run(send_usb_alerts(computer_id, is_unix, cert))

def start_ids(computer_id: int, active_int: str, is_unix: bool, cert: str):
	asyncio.run(send_traffic_alerts(computer_id, active_int, is_unix, cert))