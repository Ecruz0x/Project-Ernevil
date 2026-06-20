from pydantic import BaseModel, ConfigDict
from typing import Optional
from .add_rs_schema import Computer



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
	location_name: str
	severity: Optional[str] = None