from fastapi import FastAPI, Request, HTTPException, status, Depends, APIRouter
from sqlalchemy import select, text
from sqlalchemy.orm import Session
from ..database import dbschema
from ..database.db import Base, engine, get_db
from typing import Annotated


router = APIRouter()

