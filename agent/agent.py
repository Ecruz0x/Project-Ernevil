from computerinfo import Computer
from datetime import datetime
import requests




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
	"boot_time": localComputer.getBootTime(),
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
	data["computer_id"] = computerId
	data["last_refresh"] = str(datetime.now())
	data = dict(data)
	r = sendData(data, url = "http://127.0.0.1:8000/api/refresh")
	return True

datax = {
	"is_unix": localComputer.is_unix,
	"computer_name": localComputer.computer_name,
	"location": localComputer.computer_location,
	"users_count": localComputer.getActiveUsersCount(),
	"users": localComputer.getActiveUsers(),
	"cpu_count": localComputer.getCpuCount(),
	"cpu_usage": localComputer.getCpuUsage(),
	"memory": localComputer.getMemoryInfo(),
}
