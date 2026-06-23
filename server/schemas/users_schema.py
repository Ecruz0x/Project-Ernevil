from pydantic import BaseModel, ConfigDict, EmailStr, Field



class UserBase(BaseModel):
	model_config = ConfigDict(from_attributes = True)
	username: str = Field(min_length = 1, max_length = 50)
	email: EmailStr = Field(max_length=120)


class UserCreate(UserBase):
	password: str = Field(min_length = 8)

class UserResponse(UserBase):
	password_hash: str

class Token(BaseModel):
	access_token: str
	token_type: str