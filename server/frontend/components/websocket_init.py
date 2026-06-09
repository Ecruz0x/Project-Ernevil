import asyncio
import websockets
import subprocess
import time
import json



class frontendWebsocket:
	def __init__(self, agentid: int, uri: str):
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

	async def receiveAlerts(self):
		msg = await self.ws.recv()
		yield msg