from collectors.computer_info import Computer
import requests, json, time

currentComputer = Computer()


with open("serverdata.json", "r") as data:
	server_data = json.load(data)

server = "http://" + server_data["server_ip"] + ":" + server_data["server_port"]




def refreshComputerName(computer_id: int, fingerprint: str, oldData: dict):
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


def refreshMemInfo(computer_id: int, fingerprint: str, oldData: dict):
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
			yield True
		else:
			yield to_send_data

def refreshNetInfo(computer_id: int, fingerprint: str, oldData: dict):
	storedNetInfo = oldData["ip_addr"]
	currentNetInfo = currentComputer.getIfAddr()
	refURL = f"{server}/api/computers/net?computer_id={computer_id}"

	CrData = {
		"computer_id": computer_id,
		 "fingerprint": fingerprint
	}
	# Handle added interfaces
	added = {}
	for interface in currentNetInfo.keys():
		if interface not in storedNetInfo.keys():
			added[interface] = currentNetInfo[interface]


	# Handle removed interfaces
	removed = {}
	for interface in storedNetInfo.keys():
		if interface not in currentNetInfo.keys():
			removed[interface] = None

	# Handle updated interfaces
	updated = {}
	for interface in storedNetInfo.keys():
		if interface in currentNetInfo and currentNetInfo[interface] != storedNetInfo[interface]:
			updated[interface] = currentNetInfo[interface]
	
	if added:
		for k in added.keys():
			uDataA = CrData
			uDataA["ifname"] = k
			uDataA["ip_addr"] = added[k][1]
			print(uDataA)
			updateR = requests.patch(refURL, json = uDataA)
			if updateR.status_code <= 201:
				yield True
	if removed:
		for k in removed.keys():
			uDataR = CrData
			uDataR["ifname"] = k
			updateR = requests.delete(refURL, json = uDataR)
			if updateR.status_code <= 201:
				yield True
	if updated:
		for k in updated.keys():
			uDataU = CrData
			uDataU["ifname"] = k
			uDataU["ip_addr"] = updated[k][1]
			updateR = requests.patch(refURL, json = uDataU)
			if updateR.status_code <= 201:
				yield True
	
	oldData["ip_addr"] = currentNetInfo