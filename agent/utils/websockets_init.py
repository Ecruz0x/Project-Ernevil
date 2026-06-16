import asyncio
import websockets
import subprocess
import time
import json

class agentWebsocket:
	def __init__(self, computer_id: int, is_unix: bool, uri: str):
		self.computer_id = computer_id
		self.is_unix = is_unix
		self.uri = uri
		self.ws = None

	async def initializeSocket(self):
		max_retries = 5
		curr_retries = 0

		while curr_retries < max_retries:
			try:
				self.ws = await websockets.connect(self.uri)
				print("Websocket established!")
				return

			except Exception as e:
				curr_retries += 1
				print("Websockets Error, Retrying connection...")

	async def receiveCommands(self):
		while True:
			msg = await self.ws.recv()
			if self.is_unix:
				result = subprocess.run(
					msg.split(),
					capture_output=True,
					text=True
				)
			else:
				if msg == "shutdown now":
					msg = "Stop-Computer -Force"
				elif msg == "sudo reboot":
					msg = "Restart-Computer -Force"

				result = subprocess.run(
					["powershell.exe", "-NoProfile", "-Command", msg],
					capture_output=True,
					text=True
				)

			if result.stdout:
				await self.ws.send(result.stdout)
			elif result.stderr:
				await self.ws.send(result.stderr)
			else:
				status_code = result.returncode

				if status_code == 0:
					await self.ws.send("Command Executed!")
				else:
					await self.ws.send("Command Failed!")

	async def send_alert(self, type, category, event, **kwargs):
		await self.ws.send(json.dumps({
			"type": type,
			"category": category,
			"event": event,
			**kwargs
		}))