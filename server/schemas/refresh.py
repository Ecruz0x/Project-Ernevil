from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from .computer import MemoryInfo, NetworkingInfo, ProcessesInfo, DisksInfo, CUsersInfo


class AuthenticateComputer(BaseModel):
	### Token instead of id
	computerid: int
	fingerprint: str


class RefreshComputerName(AuthenticateComputer):
	newcomputername: str


class RefreshMemoryInfo(MemoryInfo, AuthenticateComputer):
	pass

class RefreshNetworkingInfo(NetworkingInfo, AuthenticateComputer):
	pass


class RefreshProcessesInfo(ProcessesInfo, AuthenticateComputer):
	pass

class RefreshDisksInfo(DisksInfo, AuthenticateComputer):
	pass

class CUsersInfo(CUsersInfo, AuthenticateComputer):
	pass

