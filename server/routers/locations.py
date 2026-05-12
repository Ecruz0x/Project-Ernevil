from .schemas.locations import Location, CreateLocation, CreatedLocation, GetLocations
from .database.db import Base, engine, get_db
from fastapi import FastAPI, Request, HTTPException, status, Depends, APIRouter


router = APIRouter()

@router.get("/api/locations", response_model = list[GetLocations])
def getLocations():  #### Database management Here
    return locations

