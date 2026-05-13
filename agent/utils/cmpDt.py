from ..collectors.computer_info import Computer
from datetime import datetime
import requests, sys, multiprocessing, time, logging, asyncio
from utils import fingerprint as fp

logger = logging.getLogger(__name__)

with open("serverdata.json", "r") as data:
	server_data = json.load(data)

server = server_data["server_ip"]

localComputer = Computer()


data = {
	"is_unix": localComputer.is_unix,
	"computer_name": localComputer.computer_name,
	"os": localComputer.getOS(),
	"users": localComputer.getActiveUsers(),
	"cpu_count": localComputer.getCpuCount(),
	"cpu_usage": round(localComputer.getCpuUsage(), 2),
	"memory": localComputer.getMemoryInfo(),
	"disks": localComputer.getAvailablePartitions(),
	"ip_addr": localComputer.getIfAddr(),
	"processes": localComputer.getProcesses(),
	"boot_time": localComputer.getBootTime(),
	"node_machineid": localComputer.getMachineId(),
	"fingerprint": fp.fingerprint(localComputer.getMachineId())
}



def sendData(json: dict, url: str) -> dict:
	res = requests.post(url, json = json)
	if res.status_code == 201:
		return res.json()
	else:
		print(res.status_code)
		raise ValueError("Sending Error")
	

def addComputer(data: dict) -> int:
	computer_data = data
	computer_data["is_alive"] = True
	url = f"{server}/api/computers"
	r = sendData(json = computer_data, url = url)
	computerId = r["computer_id"]
	return computerId