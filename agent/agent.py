from collectors.computer_info import Computer
from datetime import datetime
import requests, sys, multiprocessing, time, logging, asyncio

logger = logging.getLogger(__name__)


serverAgent = "http://127.0.0.1:8000"
localComputer = Computer()


data = {
	"is_unix": localComputer.is_unix,
	"computer_name": localComputer.computer_name,
	"os": localComputer.getOS(),
	"users_count": localComputer.getActiveUsersCount(),
	"users": localComputer.getActiveUsers(),
	"cpu_count": localComputer.getCpuCount(),
	"cpu_usage": round(localComputer.getCpuUsage(), 2),
	"memory": localComputer.getMemoryInfo(),
	"disk_count": localComputer.getDiskCount(),
	"disks": localComputer.getAvailablePartitions(),
	"ifcount": localComputer.getNetIfCount(),
	"ip_addr": localComputer.getIfAddr(),
	"processes_count": localComputer.getProcessesCount(),
	"processes": localComputer.getProcesses(),
	"boot_time": localComputer.getBootTime(),
	"uuid": localComputer.getUUID(),
	"node_machineid": localComputer.getMachineId()
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
	url = f"{serverAgent}/api/add_computer"
	r = sendData(json = computer_data, url = url)
	computerId = r
	return computerId


def refreshComputer(data: dict, computerId: int):
	data["computer_id"] = computerId
	data["last_refresh"] = str(datetime.now())
	data = dict(data)
	r = sendData(data, url = f"{serverAgent}/api/refresh")
	return True


def sendRefresh(computer_id: int) -> bool:
	logging.basicConfig(filename='log/changes.log', level=logging.INFO)
	while True:
		data_check = {
		"computer_id": localComputer.computer_id,
		"computer_name": localComputer.computer_name,
		"location": localComputer.computer_location,
		"users_count": localComputer.getActiveUsersCount(),
		"users": localComputer.getActiveUsers(),
		"cpu_count": localComputer.getCpuCount(),
		"cpu_usage": round(localComputer.getCpuUsage(), 2),
		"memory": localComputer.getMemoryInfo(),
		"disk_count": localComputer.getDiskCount(),
		"disks": localComputer.getAvailablePartitions(),
		"ifcount": localComputer.getNetIfCount(),
		"ip_addr": localComputer.getIfAddr(),
		"processes_count": localComputer.getProcessesCount(),
		"processes": localComputer.getProcesses(),
		"boot_time": localComputer.getBootTime(),
		}
		new_data = {}
		for k in data.keys():
			try:
				if data[k] != data_check[k]:
					new_data[k] = data_check[k]
					data[k] = data_check[k]
					logger.info(f"{datetime.now()} - Changes Detected : {k}")
			except KeyError:
				pass
		refreshComputer(new_data, computer_id)
		time.sleep(180)


def sendHeartBeat(computer_id: int):
	url = f"{serverAgent}/api/heartbeat"
	while True:
		res = requests.post(url, json = {"id": computer_id})
		print(res.text)
		time.sleep(30)


def main():
	computerId = addComputer(data)
	sendHB = multiprocessing.Process(target=sendHeartBeat, args = (computerId,))
	sendRef = multiprocessing.Process(target=sendRefresh, args = (computerId,))
	try:
		sendHB.start()
		sendRef.start()
	except KeyboardInterrupt:
		exit(1)

if __name__ == "__main__":
    sys.exit(main())