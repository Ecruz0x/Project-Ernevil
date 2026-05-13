from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class AuthenticateComputer(BaseModel):
	model_config = ConfigDict(from_attributes = True)
	computerid: int
	fingerprint: int