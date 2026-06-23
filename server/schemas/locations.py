from pydantic import BaseModel, ConfigDict
from typing import Optional
from .add_rs_schema import ComputerInfo



class Location(BaseModel):
	model_config = ConfigDict(from_attributes = True)
	location_name: str
	severity: Optional[str] = None

class CreateLocation(Location):
	pass

class CreatedLocation(BaseModel):
	model_config = ConfigDict(from_attributes = True)
	location_id: int

class GetLocations(BaseModel):
	id: int
	name: str
	severity: Optional[str] = None

class setLocation(BaseModel):
	computer_id: list[int]
	location_id: int

class removeDevLocation(BaseModel):
	computer: str

class removeLocation(BaseModel):
	location_id: int