from pydantic import BaseModel, ConfigDict


class CommandRequest(BaseModel):
	model_config = ConfigDict(from_attributes = True)
	command: str
	computer_id: int
#    signature: str

class RestartComputer(BaseModel):
	model_config = ConfigDict(from_attributes = True)
	computer_id: int

class ShutdownComputer(BaseModel):
	model_config = ConfigDict(from_attributes = True)
	computer_id: int