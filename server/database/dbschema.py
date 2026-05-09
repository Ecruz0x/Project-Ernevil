from __future__ import annotations
from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, Integer, Float, String, Text, Boolean, 
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base


class User(Base):
	__tablename__ = "users"

	id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
	username: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
	email: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)
	password: Mapped[str] = mapped_column(String(99), unique=True, nullable=False)


class Locations(Base):
	__tablename__ = "locations"
	id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
	name: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)


class ComputerInfo(Base):
	__tablename__ = "computerInfo"

	computerid: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
	computername: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
	is_unix: Mapped[bool] = mapped_column(Boolean, unique=False, nullable=False)
	os: Mapped[str] = mapped_column(String(50), unique=False, nullable=True)  ## TODO : Fix this (nullable=False)
	location: Mapped[str] = mapped_column(ForeignKey("locations.name"), nullable=True)
	is_alive: Mapped[bool] = mapped_column(Boolean, unique=False, nullable=False)