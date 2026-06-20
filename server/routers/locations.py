from ..schemas.locations import Location, CreateLocation, CreatedLocation, GetLocations
from ..database.db import Base, engine, get_db
from ..database import dbschema
from fastapi import FastAPI, Request, HTTPException, status, Depends, APIRouter
from typing import Annotated
from sqlalchemy import select, text
from sqlalchemy.orm import Session


router = APIRouter()

@router.get("", response_model = list[GetLocations])
def getLocations():  #### Database management Here
    return [{"location_name": "test"}, {"location_name": "test", "severity": "Important"}]

@router.post("", response_model = CreatedLocation)
def createLocation(location: CreateLocation, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(
        select(dbschema.Locations).where(
            dbschema.Locations.name == location.location_name
        )
    )
    existing_computer = result.scalars().first()

    if existing_computer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Adding error, please check your location name and try again",
        )

    newLocation = dbschema.Locations(
        name = location.location_name,
        severity = location.severity
        )
    db.add(newLocation)
    db.commit()
    return {"location_id": newLocation.id}
