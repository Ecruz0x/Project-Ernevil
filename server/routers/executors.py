from fastapi import FastAPI, Request, HTTPException, status, Depends, APIRouter
from ..database import dbschema
from ..database.db import Base, engine, get_db
from typing import Annotated
from sqlalchemy import text
from sqlalchemy.orm import Session



router = APIRouter()

# TODO: Implement authentication


@router.post("/commands", response_model=str)
def execCommands(command: str, computerid: int):
	pass

@router.post("/screenshot")
def captureSc(computerid: int):
	pass

@router.post("/shutdown")
def shutDownComputer(computerid: int):
	pass

@router.post("/restart")
def restartComputer(computerid: int):
	pass

