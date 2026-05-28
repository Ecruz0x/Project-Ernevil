from collectors.computer_info import Computer
import requests, json, time, copy

currentComputer = Computer()


with open("serverdata.json", "r") as data:
	server_data = json.load(data)

server = "http://" + server_data["server_ip"] + ":" + server_data["server_port"]




def updateComputerName(computer_id: int, fingerprint: str, oldData: dict):
	storedName = oldData["computer_name"]
	refURL = f"{server}/api/computers/name?computer_id={computer_id}"
	currentName = currentComputer.computer_name
	sent_data = {"computer_id": computer_id,
				"fingerprint":fingerprint,
				"name": currentName}

	if currentName != storedName:
		oldData["computer_name"] = currentName
		updateR = requests.put(refURL, data = sent_data)
		if updateR.status_code <= 201:
			yield True
		else:
			yield sent_data


def updateMemInfo(computer_id: int, fingerprint: str, oldData: dict):
	storedMemInfo = oldData["memory"]
	refURL = f"{server}/api/computers/mem?computer_id={computer_id}"
	currentMemInfo = currentComputer.getMemoryInfo()
	if currentMemInfo != storedMemInfo:
		oldData["memory"] = currentMemInfo
		to_send_data = {"computer_id": computer_id,
				"fingerprint":fingerprint,
				"totalMemory": currentMemInfo["totalMemory"],
				"available_memory": currentMemInfo["availableMemory"],
				"usage": currentMemInfo["usage"]}
		updateR = requests.put(refURL, json = to_send_data)
		if updateR.status_code <= 201:
			return True
		else:
			return to_send_data

def updateNetInfo(computer_id: int, fingerprint: str, oldData: dict):
	
	storedNetInfo = oldData["ip_addr"]
	currentNetInfo = currentComputer.getIfAddr()

	refURL = f"{server}/api/computers/net?computer_id={computer_id}"

	CrData = {
		"computer_id": computer_id,
		 "fingerprint": fingerprint
	}

	current_keys = set(currentNetInfo.keys())
	stored_keys = set(storedNetInfo.keys())
	# Handle added interfaces
	added = {}
	for k in current_keys - stored_keys:
		if "virtual" not in k:
			added[k] = currentNetInfo[k]

	# Handle removed interfaces
	removed = {}
	for k in stored_keys - current_keys:
		if "virtual" not in k:
			removed[k] = None

	# Handle updated interfaces
	updated = {}
	for k in current_keys & stored_keys:
		if currentNetInfo[k] != storedNetInfo[k]:
			updated[k] = currentNetInfo[k]
	
	success_ = True

	for k, v in added.items():
		if "virtual" not in k.lower():
			payload = copy.deepcopy(CrData)
			payload["ifname"] = k
			payload["ipaddr"] = v
			r = requests.patch(refURL, json = payload)
			storedNetInfo[k] = v
			if r.status_code == 200:
				storedNetInfo[k] = copy.deepcopy(v)
			else:
				print(f"Failed adding : {k}")
				success_ = False

	for k, v in removed.items():
		if "virtual" not in k.lower():
			payload = copy.deepcopy(CrData)
			payload["ifname"] = k
			payload["ipaddr"] = None
			r = requests.delete(refURL, json = payload)
			if r.status_code == 200:
				del storedNetInfo[k]
			else:
				print(f"Failed removing : {k}")
				success_ = False

	for k, v in updated.items():
		if "virtual" not in k.lower():
			payload = copy.deepcopy(CrData)
			payload["ifname"] = k
			payload["ipaddr"] = v
			r = requests.patch(refURL, json = payload)
			if r.status_code == 200:
				storedNetInfo[k] = copy.deepcopy(v)
			else:
				print(f"Failed updating : {k}")
				success_ = False
	if success_:
		oldData["ip_addr"] = copy.deepcopy(currentNetInfo)
	return success_


def updateDiskInfo(computer_id: int, fingerprint: str, oldData: dict):
	storedDiskInfo = oldData["disks"]
	currentDiskInfo = currentComputer.getAvailablePartitions()

	refURL = f"{server}/api/computers/hd?computer_id={computer_id}"

	CrData = {
		"computer_id": computer_id,
		 "fingerprint": fingerprint
	}

	current_keys = set(currentDiskInfo.keys())
	stored_keys = set(storedDiskInfo.keys())
	success_ = True
	# Handle added disks
	added = {}
	for k in current_keys - stored_keys:
		added[k] = currentDiskInfo[k]

	# Handle removed disks
	removed = {}
	for k in stored_keys - current_keys:
		removed[k] = None
	
	if added:
		for k, v in added.items():
			payload = copy.deepcopy(CrData)
			payload["partitionname"] = k
			payload["mountpoint"] = v["mountpoint"]
			payload["fstype"] = v["fstype"]
			r = requests.patch(refURL, json = payload)
			if r.status_code == 200:
				storedDiskInfo[k] = copy.deepcopy(v)
			else:
				print(f"Failed adding : {k}")
				success_ = False
	if removed:
		for k, v in removed.items():
			payload = copy.deepcopy(CrData)
			payload["partitionname"] = k
			r = requests.delete(refURL, json = payload)
			if r.status_code == 200:
				pass
			else:
				print(f"Failed removing : {k}")
				success_ = False

	storedDiskInfo = currentDiskInfo

	return success_


def updateProcessesInfo(computer_id: int, fingerprint: str, oldData: dict):
	refURL = f"{server}/api/computers/ps?computer_id={computer_id}"

	current_ps = currentComputer.getProcesses()
	oldData["processes"] = current_ps
	payload = current_ps

	success_ = True

	for d in payload:
		d["computer_id"] = computer_id
		d["fingerprint"] = fingerprint

	json_payload = json.dumps(payload)
	r = requests.put(refURL, json = payload)
	if r.status_code == 200:
		pass
	else:
		print(r.json())
		print(f"Failed Updating processes")
		success_ = False
	return success_


def updateUsersInfo(computer_id: int, fingerprint: str, oldData: dict):
	"""storedUserInfo = oldData["users"]
				currentUserInfo = currentComputer.getActiveUsers()"""
	pass