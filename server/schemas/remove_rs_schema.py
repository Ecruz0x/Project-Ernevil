from .update_rs_schema import AuthenticateComputer





class RemoveNetworkingInfo(AuthenticateComputer):
	model_config = ConfigDict(from_attributes = True)
	ifname: str

class UpdateDisksInfo(AuthenticateComputer):
	model_config = ConfigDict(from_attributes = True)
	partitionname: str

class CUsersInfo(CUsersInfo, AuthenticateComputer):
	model_config = ConfigDict(from_attributes = True)
	username: str