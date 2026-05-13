from ..collectors.computer_info import Computer
import requests, json

currentComputer = Computer()


with open("serverdata.json", "r") as data:
	server_data = json.load(data)

server = server_data["server_ip"]



def refreshMemInfo(computerid: int, fingerprint: str):
	refURL = f"{server}/mem?computerid={computerid}"
	currentMemInfo = currentComputer.getMemoryInfo()
	r = requests.get(refURL)
	storedMemInfo = r.data()
	if currentMemInfo != storedMemInfo:
		updateR = requests.post(refURL, data = currentMemInfo)
		return True

