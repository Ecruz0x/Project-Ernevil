from utils.cmpDt import addComputer
from utils.cmpRef import refreshMemInfo
from collectors.computer_info import Computer
from utils.fingerprint import fingerprint as fp
import sys, time

localComputer = Computer()


agentData = {
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
	"fingerprint": fp(localComputer.getMachineId())
}





"""



def sendHeartBeat(computer_id: int):
	url = f"{serverAgent}/api/heartbeat"
	while True:
		res = requests.post(url, json = {"id": computer_id})
		print(res.text)
		time.sleep(30)
"""

def main():
	while True:
		computerId = 1
		ex = refreshMemInfo(computerId, agentData["fingerprint"], agentData)
		time.sleep(5)

	"""sendHB = multiprocessing.Process(target=sendHeartBeat, args = (computerId,))
				sendRef = multiprocessing.Process(target=sendRefresh, args = (computerId,))
				try:
					sendHB.start()
					sendRef.start()
				except KeyboardInterrupt:
					exit(1)"""

if __name__ == "__main__":
    sys.exit(main())