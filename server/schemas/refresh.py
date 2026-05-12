from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime



class RefreshComputerName(BaseModel):
	### Token instead of id
	computerid: int
	computername: str