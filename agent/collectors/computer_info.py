import psutil, ifaddr, ipaddress, requests, os, json, socket, machineid, uuid, platform, getmac
from datetime import datetime
import wmi
import usb.core
import usb.util




class Computer:

	def __init__(self, computer_location: str=None):
		self.computer_name = socket.gethostname()
		self.computer_location = computer_location
		if os.name == 'posix':
			import pwd
			self.is_unix = True
		else:
			self.is_unix = False

	def getActiveUsers(self) -> list[str]:
		activeUsers = []
		if self.is_unix:
			for entry in pwd.getpwall():
				activeUsers.append(entry.pw_name)
		else:
			for user in psutil.users():
				activeUsers.append(user[0])
		return activeUsers


	@staticmethod
	def getCpuCount() -> int:
		cpu_count = psutil.cpu_count()
		return int(cpu_count)

	@staticmethod
	def getCpuUsage() -> float:
		return float(psutil.cpu_percent(interval=1))


	@staticmethod
	def getMemoryInfo() -> dict:
		ram = psutil.virtual_memory()
		return {"totalMemory": ram.total / (1024 ** 3),
				"availableMemory": ram.available / (1024 ** 3),
				"usage": ram.percent}


	def getAvailablePartitions(self) -> dict:
		diskPartitions = psutil.disk_partitions(all=False)
		disks = {}
		if self.is_unix:
			for i in diskPartitions:
				disks[f"{i[0]}"] = {"mountpoint": i[1], "fstype": i[2]}
		else:
			for i in diskPartitions:
				disks[f"{i[0]}"] = {"mountpoint": i[1], "fstype": i[2]}
		return disks


	@staticmethod
	def getIfAddr() -> dict:
		adapters = ifaddr.get_adapters()
		stats = psutil.net_if_stats()
		adapters_ = {}
		for adapter in adapters:
			for ip in adapter.ips:
				addr = ip.ip[0] if isinstance(ip.ip, tuple) else ip.ip
				addr = str(addr)
				if "." not in addr:
					continue
				else:
					adapters_[adapter.nice_name] = addr
		return adapters_


	@staticmethod
	def getProcesses() -> list:
		processes = []

		for proc in psutil.process_iter(['pid', 'name', 'username']):
		    processes.append(proc.info)
		return processes

	@staticmethod
	def getBootTime() -> str:
		unix_boottime = psutil.boot_time()
		boot_time = datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
		return boot_time

	@staticmethod
	def getMachineId() -> str:
		node_machineid = machineid.id()
		return str(node_machineid)

	@staticmethod
	def getOS() -> str:
		return platform.system()

	@staticmethod
	def getMAC() -> str:
		return getmac.get_mac_address()

	def getUSBDevices(self) -> str:
		usbDev = {}
		if self.is_unix:
			devices = usb.core.find(find_all=True)
			for device in devices:
				usbDev["vendor_id"] = hex(device.idVendor)
				usbDev["product_id"] = hex(device.idProduct)
		else:
			#shutil.copy("./required_drivers/*", "C:\\Windows\\System32")
			devices = usb.core.find(find_all=True)
			for device in devices:
				usbDev["vendor_id"] = hex(device.idVendor)
				usbDev["product_id"] = hex(device.idProduct)
		return usbDev
