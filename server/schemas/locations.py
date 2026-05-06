from pydantic import BaseModel
from typing import Optional
from .computer import Computer



class Location(BaseModel):
	location_name: str
	severity: Optional[str] = None
	computers: list[Computer] = []