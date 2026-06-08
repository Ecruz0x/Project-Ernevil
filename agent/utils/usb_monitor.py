from usbmonitor import USBMonitor
from usbmonitor.attributes import ID_MODEL, ID_MODEL_ID, ID_VENDOR_ID, ID_VENDOR_FROM_DATABASE
import time, asyncio
from queue import Queue


events = Queue()

device_info_str = lambda device_info: f"{device_info[ID_MODEL]} ({device_info[ID_MODEL_ID]} - {device_info[ID_VENDOR_ID]})"
# Define the `on_connect` and `on_disconnect` callbacks
def on_connect(device_id, device_info):
    try:
        ct = {
            "manufacturer": device_info.get(ID_VENDOR_FROM_DATABASE),
            "product": device_info.get(ID_MODEL),
            "vendor_id": device_info.get(ID_VENDOR_ID),
            "product_id": device_info.get(ID_MODEL_ID)
        }
        events.put(("connect", ct))
    except Exception as e:
        print("Cannot retrieve current device information")
def on_disconnect(device_id, device_info):
    try:
        dt = {
            "manufacturer": device_info.get(ID_VENDOR_FROM_DATABASE),
            "product": device_info.get(ID_MODEL),
            "vendor_id": device_info.get(ID_VENDOR_ID),
            "product_id": device_info.get(ID_MODEL_ID)
        }
        events.put(("disconnect", dt))
    except Exception as e:
        print("Cannot retrieve current device information")


async def startUSBMonitoring():
    try:
        monitor = USBMonitor()
        monitor.start_monitoring(on_connect=on_connect, on_disconnect=on_disconnect)
        while True:
            event = await asyncio.to_thread(events.get)
            yield event
    except KeyboardInterrupt:
        print("Stopping...")
        monitor.stop_monitoring()