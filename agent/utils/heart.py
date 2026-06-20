import requests, time



def sendBeat(computer_id: int, fingerprint: str, heartbeat_interval: int, serverAgent: str, cert: str):
	url = f"{serverAgent}/api/computers/heartbeat"
	CrData = {
		"computer_id": computer_id,
		 "fingerprint": fingerprint
	}
	while True:
		time.sleep(heartbeat_interval)
		try:
			res = requests.post(url, json = CrData, verify=cert)
		except Exception as e:
			print("Error: Could not establish connection")


