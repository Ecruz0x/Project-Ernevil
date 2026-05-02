from pydantic import BaseModel, ConfigDict
from typing import Optional


class Computer(BaseModel):
	is_unix: bool
	computer_name: str
	location: str
	users_count: int
	users: list
	cpu_count: int
	cpu_usage: float
	memory: dict
	disk_count: int
	disks: dict
	ifcount: int 							# Number of ip interfaces
	ip_addr: dict							# IP Address per Interface
	processes_count: int
	processes: list
	boot_time: str
	is_alive: bool

class CreateComputer(Computer):
	pass

class RefreshComputer(BaseModel):
	computer_id: int
	is_unix: Optional[bool]
	computer_name: Optional[str]
	location: Optional[str]
	users_count: Optional[int]
	users: Optional[list]
	cpu_count: Optional[int]
	cpu_usage: Optional[float]
	memory: Optional[dict]
	disk_count: Optional[int]
	disks: Optional[dict]
	ifcount: Optional[int]
	ip_addr: Optional[dict]
	processes_count: Optional[int]
	processes: Optional[list]
	boot_time: Optional[str]
	is_alive: Optional[bool]


class ComputerWithID(Computer):
	model_config = ConfigDict(from_attributes = True)
	computer_id: int


class Location(BaseModel):
	location_name: str
	severity: str
	computers: list[Computer] = []

