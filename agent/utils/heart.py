import requests, time

serverAgent = "http://127.0.0.1:8000"

def sendBeat(computer_id: int, fingerprint: str):
	url = f"{serverAgent}/api/computers/heartbeat"
	CrData = {
		"computer_id": computer_id,
		 "fingerprint": fingerprint
	}
	while True:
		time.sleep(15)
		res = requests.post(url, json = CrData)

