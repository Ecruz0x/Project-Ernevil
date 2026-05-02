import psutil, ifaddr, ipaddress, datetime, requests, os, json

class Computer:

	def __init__(self, computer_name: str, computer_location: str):
		self.computer_name = computer_name
		self.computer_location = computer_location
		if os.name == 'posix':
			self.is_unix = True
		else:
			self.is_unix = False

	@staticmethod
	def getActiveUsersCount() -> int:
		return len(psutil.users())

	@staticmethod
	def getActiveUsers() -> list[str]:
		activeUsers = []
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


	@staticmethod
	def getDiskCount() -> int:
		return len(psutil.disk_partitions(all=False))

	def getAvailablePartitions(self) -> dict:
		diskPartitions = psutil.disk_partitions(all=False)
		disks = {}
		if self.is_unix:
			x = 0
			for i in diskPartitions:
				disks[f"disk {x}"] = {"device": i[0], "mountpoint": "", "fstype": i[2]}
				x += 1
		else:
			x = 0
			for i in diskPartitions:
				disks[f"disk {x}"] = {"device": i[0], "mountpoint": i[1], "fstype": i[2]}
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


localComputer = Computer("PC1", "Salle1")


data = {
	"is_unix": localComputer.is_unix,
	"computer_name": localComputer.computer_name,
	"location": localComputer.computer_location,
	"users_count": localComputer.getActiveUsersCount(),
	"users": localComputer.getActiveUsers(),
	"cpu_count": localComputer.getCpuCount(),
	"cpu_usage": localComputer.getCpuUsage(),
	"memory": localComputer.getMemoryInfo(),
	"disk_count": localComputer.getDiskCount(),
	"disks": localComputer.getAvailablePartitions(),
	"ifcount": localComputer.getNetIfCount(),
	"ip_addr": localComputer.getIfAddr(),
	"processes_count": localComputer.getProcessesCount(),
	"processes": localComputer.getProcesses(),
	"boot_time": localComputer.getBootTime()
}


def sendData(json: dict, url: str) -> dict:
	res = requests.post(url, json = json)
	if res.status_code == 201:
		return res.json()
	else:
		print(res.status_code)
		raise ValueError("Sending Error")
	

def addComputer(data: dict) -> int:
	data["is_alive"] = True
	url = "http://127.0.0.1:8000/api/add_computer"
	r = sendData(json = data, url = url)
	computerId = r["computer_id"]
	return computerId

def refreshComputer(data: dict, computerId: int):
	urlC = "http://127.0.0.1:8000/api/refresh"
	res = requests.get(url)
	for i in res.json():
		if i["computer_id"] == computerId:
			data["computer_id"] = computerId
			sendData(data, url = "http://127.0.0.1:8000/api/refresh")
			return True
	else:
		raise ValueError("Refresh Error: Computer not found")


computerId = addComputer(data)

