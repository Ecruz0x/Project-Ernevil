import psutil, ifaddr, ipaddress, requests, os, json, socket, machineid, uuid, pwd, platform
from datetime import datetime



class Computer:

	def __init__(self, computer_location: str=None):
		self.computer_name = socket.gethostname()
		self.computer_location = computer_location
		if os.name == 'posix':
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
			x = 0
			for i in diskPartitions:
				disks[f"disk {x}"] = {"device": i[0], "mountpoint": i[1], "fstype": i[2]}
				x += 1
		else:
			x = 0
			for i in diskPartitions:
				disks[f"disk {x}"] = {"device": i[0], "mountpoint": i[0], "fstype": i[2]}
				x += 1

		return disks


	@staticmethod
	def getIfAddr() -> dict:
		adapters = ifaddr.get_adapters()

		adapters_ = {}

		for adapter in adapters:
			if adapter.ips:
				adapters_[adapter.nice_name] = []
				for ip in adapter.ips:
					if isinstance(ip.ip, tuple):
						ip = ip.ip[0]
					else:
						ip = ip.ip
						
					adapters_[adapter.nice_name].append(str(ipaddress.ip_address((f"{ip}"))))
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
	def getUUID() -> str:
		return str(uuid.getnode())