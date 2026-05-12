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

class RefreshComputer(BaseModel):
	model_config = ConfigDict(from_attributes = True)
	is_unix: Optional[bool] = None
	computer_name: Optional[str] = None
	location: Optional[str] = None
	users_count: Optional[int] = None
	users: Optional[list] = None
	cpu_count: Optional[int] = None
	cpu_usage: Optional[float] = None
	memory: Optional[dict] = None
	disk_count: Optional[int] = None
	disks: Optional[dict] = None
	ifcount: Optional[int] = None
	ip_addr: Optional[dict] = None
	processes_count: Optional[int] = None
	processes: Optional[list] = None
	boot_time: Optional[str] = None
	computer_id: str
	last_refresh: str


class ComputerCreated(Computer):
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
	totalMemory: float
	available_memory: float
	usage: float

class NetworkingInfo(BaseModel):
	ifname: str
	ipaddr: str

class ProcessesInfo(BaseModel):
	pid: int
	user: str
	process_name: str

class disksInfo(Base):
	partitionname: str
	mountpoint: str
	fstype: str

class CUsersInfo(Base):
	username: str
