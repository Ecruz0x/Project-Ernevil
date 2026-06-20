from ..schemas.locations import Location, CreateLocation, CreatedLocation, GetLocations, setLocation
from ..database.db import Base, engine, get_db
from ..database import dbschema
from fastapi import FastAPI, Request, HTTPException, status, Depends, APIRouter
from typing import Annotated
from sqlalchemy import select, text
from sqlalchemy.orm import Session


router = APIRouter()

@router.get("", response_model = list[GetLocations])
def getLocations(db: Annotated[Session, Depends(get_db)]):  #### Database management Here
    result = db.execute(
        select(
            dbschema.Locations.id,
            dbschema.Locations.name,
            dbschema.Locations.severity
        )
    )

    locations = result.mappings().all()
    return locations

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

@router.delete("", response_model = bool)
def removeLocation():
    pass

@router.post("/set", response_model = bool)
def setLocation(data: setLocation, db: Annotated[Session, Depends(get_db)]):
    for ids in data.computer_id:
        computer = (
            db.query(dbschema.ComputerInfo)
            .filter(dbschema.ComputerInfo.computer_id == ids)
            .first()
        )
        if computer:
            computer.location_id = data.location_id
            db.commit()
            return True