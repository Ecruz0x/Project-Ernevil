from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class AuthenticateComputer(BaseModel):
	model_config = ConfigDict(from_attributes = True)
	computer_id: int
	fingerprint: str

class AuthUpdates(BaseModel):
	model_config = ConfigDict(from_attributes = True)
	computer_id: int
	key: str