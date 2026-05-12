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



class ComputerCreated(Computer):
	### Token instead of returning a computerid
	model_config = ConfigDict(from_attributes = True)
	computer_id: int
	computername: str
	added_on: datetime


class ComputerInfo(BaseModel):
	model_config = ConfigDict(from_attributes = True)
	computerid: int
	computername: str
	is_unix: bool
	os: str
	boottime: datetime
	is_alive: bool
	node_machineid: str
	added_on: datetime
	fingerprint: str

class SpecificComputerInfo(BaseModel):
	model_config = ConfigDict(from_attributes = True)
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
	user: str
	process_name: str

class disksInfo(Base):
	model_config = ConfigDict(from_attributes = True)
	partitionname: str
	mountpoint: str
	fstype: str

class CUsersInfo(Base):
	model_config = ConfigDict(from_attributes = True)
	username: str
