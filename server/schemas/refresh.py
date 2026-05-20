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


class RefreshMemoryInfo(AuthenticateComputer, MemoryInfo):
	pass

class RefreshNetworkingInfo(AuthenticateComputer):
	model_config = ConfigDict(from_attributes = True)
	newNetInfo: dict


class RefreshProcessesInfo(ProcessesInfo, AuthenticateComputer):
	pass

class RefreshDisksInfo(DisksInfo, AuthenticateComputer):
	pass

class CUsersInfo(CUsersInfo, AuthenticateComputer):
	pass

