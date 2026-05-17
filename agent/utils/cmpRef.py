from collectors.computer_info import Computer
import requests, json, time

currentComputer = Computer()


with open("serverdata.json", "r") as data:
	server_data = json.load(data)

server = server_data["server_ip"]



def refreshMemInfo(computerid: int, fingerprint: str, oldData: dict):
	storedMemInfo = oldData["memory"]
	refURL = f"{server}/mem?computerid={computerid}"
	currentMemInfo = currentComputer.getMemoryInfo()
	print(currentComputer)
	print(oldData["memory"])
	if currentMemInfo != storedMemInfo:
		oldData["memory"] = currentMemInfo
		updateR = requests.post(refURL, data = currentMemInfo)
		if updateR.status_code <= 201:
			print(updateR.status_code)
			yield True
		else:
			yield False



