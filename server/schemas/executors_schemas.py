from pydantic import BaseModel, ConfigDict


class CommandRequest(BaseModel):
	model_config = ConfigDict(from_attributes = True)
	command: str
	computer_id: int
#    signature: str

