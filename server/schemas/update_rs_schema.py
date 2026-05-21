from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime
from .add_rs_schema import MemoryInfo, NetworkingInfo, ProcessesInfo, DisksInfo, CUsersInfo


class AuthenticateComputer(BaseModel):
	### Token instead of id
	computer_id: int
	fingerprint: str


class UpdateComputerName(AuthenticateComputer):
	newcomputername: str


class UpdateMemoryInfo(AuthenticateComputer, MemoryInfo):
	pass

class UpdateNetworkingInfo(AuthenticateComputer):
	model_config = ConfigDict(from_attributes = True)
	ifname: str
	ipaddr: str | None = Field(default=None)


class UpdateProcessesInfo(ProcessesInfo, AuthenticateComputer):
	pass

class UpdateDisksInfo(DisksInfo, AuthenticateComputer):
	pass

class CUsersInfo(CUsersInfo, AuthenticateComputer):
	pass

