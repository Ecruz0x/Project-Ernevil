from utils.initializer import initializeComputerInfo
from utils.updater import sendFullUpdates
from utils.heart import sendBeat
from collectors.computer_info import Computer
from utils.fingerprint import fingerprint as fp
import sys, time, json, requests, copy, multiprocessing



with open("serverdata.json", "r") as data:
	server_data = json.load(data)

server = "http://" + server_data["server_ip"] + ":" + server_data["server_port"]

localComputer = Computer()


currentAgentInfo = {
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




# Update interval, Retry time, HB intervals
with open("./agentdata.json", "r") as agentdata:
	agent_data = json.load(agentdata)



def main():
	cagentdata = copy.deepcopy(currentAgentInfo)
	computer_id = initializeComputerInfo(cagentdata)

	"""if agent_data["agentid"]:
					agid = agent_data["agentid"]
					isAddedComputer = requests.get(f"{server}/api/computers?computer_id={agid}")
					if isAddedComputer:
						computer_id = agid
					else:
						computer_id = addComputer(currentAgentInfo)
						agent_data["agentid"] = computer_id"""
	

	beat = multiprocessing.Process(target=sendBeat, args = (computer_id, cagentdata["fingerprint"]))
	updates = multiprocessing.Process(target=sendFullUpdates, args = (computer_id, cagentdata))
	try:
		beat.start()
		updates.start()
	except KeyboardInterrupt:
		exit(1)


if __name__ == "__main__":
    sys.exit(main())