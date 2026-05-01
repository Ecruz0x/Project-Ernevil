import psutil, pwd, ifaddr, datetime




class Computer:

	def __init__(self, computer_id: int, computer_name: str, computer_location: str, is_unix: bool):
		self.computer_id = computer_id
		self.computer_name = computer_name
		self.computer_location = computer_location
		self.is_unix = is_unix

	@staticmethod
	def getActiveUsersCount() -> int:
		return count = len(psutil.users())

	@staticmethod
	def getActiveUsers() -> set[str]:
		activeUsers = []
		for user in psutil.users():
			activeUsers = user[0]
		return set(activeUsers)


	@staticmethod
	def getCpuCount() -> cpu_count:
		cpu_count = psutil.cpu_count()
		return cpu_count

	@staticmethod
	def getCpuUsage() -> float:
		return psutil.cpu_percent(interval=1)


	@staticmethod
	def getMemoryInfo() -> dict:
		ram = psutil.virtual_memory()
		return {"totalMemory": ram.total / (1024 ** 3),
				"availableMemory": ram.available / (1024 ** 3),
				"usage": ram.percent}


	@staticmethod
	def getDiskCount() -> int:
		return len(psutil.disk_partitions(all=False))

	def getAvailablePartitions(self) -> dict:
		diskPartitions = psutil.disk_partitions(all=False)
		disks = {}
		if self.is_unix:
			x = 0
			for i in diskPartitions:
				d[f"disk {x}"] = {"device": i[0], "mountpoint": "", "fstype": i[2]}
				x += 1
		else:
			x = 0
			for i in diskPartitions:
				d[f"disk {x}"] = {"device": i[0], "mountpoint": i[1], "fstype": i[2]}
				x += 1

		return disks

	@staticmethod
	def getNetIfCount() -> int:
		return len(psutil.net_if_addrs())-1                     # Counts localhost interface too, that's the reason behind the -1


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
	def getProcessesCount() -> int:
		return len(psutil.pids())

	@staticmethod
	def getProcesses() -> list:
		processes = []

		for proc in psutil.process_iter(['pid', 'name', 'username']):
		    processes.append(proc.info)
		return processes

	@staticmethod
	def getBootTime() -> str:
		unix_boottime = psutil.boot_time()
		boot_time = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
		return boot_time