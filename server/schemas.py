from pydantic import BaseModel, ConfigDict

class Computer(BaseModel):
	is_unix: bool = False
	computer_name: str
	location: str
	users_count: int
	users: list
	cpu_count: int
	cpu_usage: float
	memory: dict
	disk_count: int
	disks: list[str]
	ifcount: int 							# Number of ip interfaces
	ip_addr: dict							# IP Address per Interface
	processes_count: int
	processes: list
	boot_time: str

class CreateComputer(Computer):
	pass


class ComputerWithID(Computer):
	model_config = ConfigDict(from_attributes = True)
	computer_id: int


class Location(BaseModel):
	location_name: str
	severity: str
	computers: list[Computer] = []

