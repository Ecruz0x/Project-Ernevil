from collectors.computer_info import Computer
import requests, json, time

currentComputer = Computer()


with open("serverdata.json", "r") as data:
	server_data = json.load(data)

server = "http://" + server_data["server_ip"] + ":" + server_data["server_port"]




def refreshComputerName(computerid: int, fingerprint: str, oldData: dict):
	storedName = oldData["computer_name"]
	refURL = f"{server}/api/computers/name?computerid={computerid}"
	currentName = currentComputer.computer_name
	sent_data = {"computerid": computerid,
				"fingerprint":fingerprint,
				"name": currentName}

	if currentName != storedName:
		oldData["computer_name"] = currentName
		updateR = requests.post(refURL, data = sent_data)
		if updateR.status_code <= 201:
			yield True
		else:
			yield sent_data



def refreshMemInfo(computerid: int, fingerprint: str, oldData: dict):
	storedMemInfo = oldData["memory"]
	refURL = f"{server}/api/computers/mem?computerid={computerid}"
	currentMemInfo = currentComputer.getMemoryInfo()
	if currentMemInfo != storedMemInfo:
		oldData["memory"] = currentMemInfo
		to_send_data = {"computerid": computerid,
				"fingerprint":fingerprint,
				"totalMemory": currentMemInfo["totalMemory"],
				"available_memory": currentMemInfo["availableMemory"],
				"usage": currentMemInfo["usage"]}
		updateR = requests.post(refURL, json = to_send_data)
		if updateR.status_code <= 201:
			yield True
		else:
			yield to_send_data

def refreshNetInfo(computerid: int, fingerprint: str, oldData: dict):
	storedNetInfo = oldData["ip_addr"]
	currentMemInfo = currentComputer.getMemoryInfo()
	refURL = f"{server}/api/computers/mem?computerid={computerid}"
	sent_data = {"computerid": computerid,
				"fingerprint":fingerprint,
				"totalMemory": currentMemInfo["totalMemory"],
				"available_memory": currentMemInfo["availableMemory"],
				"usage": currentMemInfo["usage"]}
	if currentMemInfo != storedMemInfo:
		oldData["memory"] = currentMemInfo
		updateR = requests.post(refURL, data = sent_data)
		if updateR.status_code <= 201:
			yield True
		else:
			yield sent_data