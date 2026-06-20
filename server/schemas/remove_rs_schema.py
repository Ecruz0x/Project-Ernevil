from .update_rs_schema import AuthenticateComputer, UCUsersInfo
from pydantic import BaseModel, ConfigDict, Field




class RemoveNetworkingInfo(AuthenticateComputer):
	model_config = ConfigDict(from_attributes = True)
	ifname: str

class RemoveDisksInfo(AuthenticateComputer):
	model_config = ConfigDict(from_attributes = True)
	partitionname: str

class RCUsersInfo(UCUsersInfo, AuthenticateComputer):
	pass

class removeLocation(BaseModel):
	model_config = ConfigDict(from_attributes = True)
	location_name: str