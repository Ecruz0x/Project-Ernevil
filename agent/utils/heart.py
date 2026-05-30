import requests, time



def sendBeat(computer_id: int, fingerprint: str, heartbeat_interval: int, serverAgent: str):
	url = f"{serverAgent}/api/computers/heartbeat"
	CrData = {
		"computer_id": computer_id,
		 "fingerprint": fingerprint
	}
	while True:
		time.sleep(heartbeat_interval)
		res = requests.post(url, json = CrData)

