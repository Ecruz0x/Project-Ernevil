import requests, time


def sendBeat(computer_id: int):
	url = f"{serverAgent}/api/computers/heartBeat"
	while True:
		res = requests.post(url, json = {"id": computer_id})
		print(res.text)
		time.sleep(30)