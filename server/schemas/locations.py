from pydantic import BaseModel
from typing import Optional
from .computer import Computer



class Location(BaseModel):
	model_config = ConfigDict(from_attributes = True)
	location_name: str
	severity: Optional[str] = None
	computers: list[Computer] = []

class CreateLocation(Location):
	pass

class CreatedLocation(Location):
	model_config = ConfigDict(from_attributes = True)
	location_id: int

class GetLocations(CreatedLocation):
	location_name: str
	severity: Optional[str] = None