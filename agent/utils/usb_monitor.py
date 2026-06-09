from usbmonitor import USBMonitor
from usbmonitor.attributes import (
    ID_MODEL,
    ID_MODEL_ID,
    ID_VENDOR_ID,
    ID_VENDOR_FROM_DATABASE
)
import asyncio

events = asyncio.Queue()
loop = None

device_info_str = lambda device_info: (
    f"{device_info[ID_MODEL]} "
    f"({device_info[ID_MODEL_ID]} - {device_info[ID_VENDOR_ID]})"
)


def on_connect(device_id, device_info):
    global loop

    try:
        ct = {
            "manufacturer": device_info.get(ID_VENDOR_FROM_DATABASE),
            "product": device_info.get(ID_MODEL),
            "vendor_id": device_info.get(ID_VENDOR_ID),
            "product_id": device_info.get(ID_MODEL_ID)
        }

        if loop is not None:
            loop.call_soon_threadsafe(
                events.put_nowait,
                ("connect", ct)
            )

    except Exception as e:
        print(f"USB connect error: {e}")


def on_disconnect(device_id, device_info):
    global loop

    try:
        dt = {
            "manufacturer": device_info.get(ID_VENDOR_FROM_DATABASE),
            "product": device_info.get(ID_MODEL),
            "vendor_id": device_info.get(ID_VENDOR_ID),
            "product_id": device_info.get(ID_MODEL_ID)
        }

        if loop is not None:
            loop.call_soon_threadsafe(
                events.put_nowait,
                ("disconnect", dt)
            )

    except Exception as e:
        print(f"USB disconnect error: {e}")


async def launchUsbMon():
    global loop

    loop = asyncio.get_running_loop()

    monitor = USBMonitor()

    try:
        monitor.start_monitoring(
            on_connect=on_connect,
            on_disconnect=on_disconnect
        )

        while True:
            event = await events.get()
            yield event

    finally:
        print("Stopping USB monitor...")
        monitor.stop_monitoring()