from datetime import timezone, datetime, timedelta
import jwt
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from .config import settings
from typing import Annotated
from sqlalchemy import text, select
from fastapi import HTTPException, status, Depends
from .database import dbschema
from .database.db import Base, engine, get_db
from sqlalchemy.orm import Session



password_hash = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/users/token")

def hash_password(password: str) -> str:
	return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
	return password_hash.verify(plain_password, hashed_password)



def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
	to_encode = data.copy()
	if expires_delta:
		expire = datetime.now(timezone.utc) + expires_delta
	else:
		expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
	to_encode.update({"exp": expire})
	encoded_jwt = jwt.encode(to_encode, settings.secret_key.get_secret_value(), algorithm=settings.algorithm)
	return encoded_jwt

def verify_access_token(token: str) -> str | None:
	"""verify a jwt tocken and return the subject (userid) if valid."""
	try:
		payload = jwt.decode(token, settings.secret_key.get_secret_value(), algorithms=[settings.algorithm], options={"require": ["exp", "sub"]})
	except jwt.InvalidTokenError:
		return None
	else:
		return payload.get("sub")

def check_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Annotated[Session, Depends(get_db)]):
	user_id = verify_access_token(token)
	if user_id is None:
		raise HTTPException (
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Invalid access token"
		)
	try:
		user_id_int = int(user_id)
	except (TypeError, ValueError):
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token", headers={"WWW-Authenticate": "Bearer"})

	result = db.execute(select(dbschema.Users).where(dbschema.Users.id == user_id_int))
	user = result.scalars().first()
	if not user:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found", headers={"WWW-Authenticate": "Bearer"})
	return user

ValidUser = Annotated[dbschema.Users, Depends(check_current_user)]