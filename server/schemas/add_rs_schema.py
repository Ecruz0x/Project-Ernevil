from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime



class Computer(BaseModel):
	model_config = ConfigDict(from_attributes = True)
	is_unix: bool
	os: str
	computer_name: str
	users: list
	cpu_count: int
	cpu_usage: float
	memory: dict
	disks: dict
	ip_addr: dict							# IP Address per Interface
	processes: list	
	boot_time: datetime
	node_machineid: str
	fingerprint: str


class CreateComputer(Computer):
	pass



class ComputerCreated(BaseModel):
	### Token instead of returning a computerid
	model_config = ConfigDict(from_attributes = True)
	computer_id: int
	computername: str
	added_on: datetime


class ComputerInfo(BaseModel):
	model_config = ConfigDict(from_attributes = True)
	computer_id: int
	computername: str
	is_unix: bool
	os: str
	boottime: datetime
	is_alive: bool
	node_machineid: str
	added_on: datetime
	fingerprint: str

class MemoryInfo(BaseModel):
	model_config = ConfigDict(from_attributes = True)
	totalMemory: float
	available_memory: float
	usage: float

class NetworkingInfo(BaseModel):
	model_config = ConfigDict(from_attributes = True)
	ifname: str
	ipaddr: str

class ProcessesInfo(BaseModel):
	model_config = ConfigDict(from_attributes = True)
	pid: int
	username: Optional[str] = None
	name: str

class DisksInfo(BaseModel):
	model_config = ConfigDict(from_attributes = True)
	partitionname: str
	mountpoint: str
	fstype: str

class CUsersInfo(BaseModel):
	model_config = ConfigDict(from_attributes = True)
	username: str

class CPUInfo(BaseModel):
	model_config = ConfigDict(from_attributes = True)
	usage: float