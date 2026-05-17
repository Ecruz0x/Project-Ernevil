from collectors.computer_info import Computer
import requests, json, time

currentComputer = Computer()


with open("serverdata.json", "r") as data:
	server_data = json.load(data)

server = "http://" + server_data["server_ip"] + ":" + server_data["server_port"]




def refreshMemInfo(computerid: int, fingerprint: str, oldData: dict):
	storedMemInfo = oldData["memory"]
	refURL = f"{server}/api/computers/mem?computerid={computerid}"
	currentMemInfo = currentComputer.getMemoryInfo()
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



