from fastapi import FastAPI, Request, HTTPException, status, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from ..schemas.users_schema import UserBase, UserCreate, Token, UserResponse
from datetime import datetime, timedelta
from sqlalchemy import select, text, func
from ..auth import create_access_token, verify_access_token, oauth2_scheme, verify_password, hash_password
from ..config import settings
from sqlalchemy.orm import Session
from ..database import dbschema
from ..database.db import Base, engine, get_db
from typing import Annotated
import time, asyncio, logging


router = APIRouter()


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Annotated[Session, Depends(get_db)]):
	result = db.execute(select(dbschema.Users).where(func.lower(dbschema.Users.username) == user.username.lower()))
	existing_user = result.scalars().first()
	if existing_user:
		raise HTTPException (
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="Username Already exists"
		)
	result = db.execute(select(dbschema.Users).where(func.lower(dbschema.Users.email) == user.email.lower()))
	existing_email = result.scalars().first()
	if existing_email:
		raise HTTPException (
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="Email Already exists"
		)
	user = dbschema.Users(username = user.username, email = user.email.lower(), password_hash=hash_password(user.password))
	db.add(user)
	db.commit()
	db.refresh(user)
	return user


@router.get("/count")
def get_user_count(db: Annotated[Session, Depends(get_db)]):
    count = db.scalar(select(func.count()).select_from(dbschema.Users))
    return {"count": count}


@router.post("/token", response_model=Token)
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[Session, Depends(get_db)]):
	result = db.execute(select(dbschema.Users).where(func.lower(dbschema.Users.email) == form_data.username.lower()))
	user = result.scalars().first()
	if not user or not verify_password(form_data.password, user.password_hash):
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password", headers={"WWW-Authenticate": "Bearer"})
	access_token_expires = timedelta(minutes = settings.access_token_expire_minutes)
	access_token = create_access_token(data={"sub": str(user.id)}, expires_delta=access_token_expires)
	return Token(access_token = access_token, token_type = "bearer")


@router.get("/me", response_model=UserResponse)
def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Annotated[Session, Depends(get_db)]):
	user_id = verify_access_token(token)
	if user_id is None:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token", headers={"WWW-Authenticate": "Bearer"})
	try:
		user_id_int = int(user_id)
	except (TypeError, ValueError):
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token", headers={"WWW-Authenticate": "Bearer"})

	result = db.execute(select(dbschema.Users).where(dbschema.Users.id == user_id_int))
	user = result.scalars().first()
	if not user:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found", headers={"WWW-Authenticate": "Bearer"})
	return user

