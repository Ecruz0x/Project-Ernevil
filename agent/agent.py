







def sendHeartBeat(computer_id: int):
	url = f"{serverAgent}/api/heartbeat"
	while True:
		res = requests.post(url, json = {"id": computer_id})
		print(res.text)
		time.sleep(30)
"""

def main():
	computerId = addComputer(data)
	print(computerId)
	"""sendHB = multiprocessing.Process(target=sendHeartBeat, args = (computerId,))
				sendRef = multiprocessing.Process(target=sendRefresh, args = (computerId,))
				try:
					sendHB.start()
					sendRef.start()
				except KeyboardInterrupt:
					exit(1)"""

if __name__ == "__main__":
    sys.exit(main())