from collectors.computer_info import Computer
from datetime import datetime
import requests, sys, multiprocessing, time, logging, asyncio, json
from utils import fingerprint as fp

logger = logging.getLogger(__name__)

with open("serverdata.json", "r") as data:
	server_data = json.load(data)

server = "https://" + server_data["server_ip"] + ":" + server_data["server_port"]

localComputer = Computer()



def sendData(json: dict, url: str, cert: str) -> dict:
	res = requests.post(url, json = json, verify=cert)
	if res.status_code == 201:
		return res.json()
	else:
		print(res.status_code)
		raise ValueError("Sending Error")
	

def initializeComputerInfo(data: dict, cert: str) -> int:
	computer_data = data
	computer_data["is_alive"] = True
	url = f"{server}/api/computers"
	r = sendData(json = computer_data, url = url, cert = cert)
	computer_id = r["computer_id"]
	return computer_id