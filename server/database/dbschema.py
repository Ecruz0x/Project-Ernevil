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
	password: Mapped[str] = mapped_column(String(99), unique=False, nullable=False)


class Locations(Base):
	__tablename__ = "locations"
	id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
	name: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)


class ComputerInfo(Base):
	__tablename__ = "computerInfo"

	computerid: Mapped[str] = mapped_column(String(256), primary_key=True, index=True)
	computername: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
	is_unix: Mapped[bool] = mapped_column(Boolean, unique=False, nullable=False)
	location: Mapped[str] = mapped_column(ForeignKey("locations.name"), nullable=True, unique=False)
	os: Mapped[str] = mapped_column(String(50), unique=False, nullable=True)  ## TODO : Fix this (nullable=False)
	boottime: Mapped[datetime] = mapped_column(DateTime, unique = False, nullable=False)
	is_alive: Mapped[bool] = mapped_column(Boolean, unique=False, nullable=False)
	node_machineid: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)


class MemoryInfo(Base):
	__tablename__ = "memoryinfo"

	computerid: Mapped[str] = mapped_column(primary_key=True, ForeignKey("computerInfo.computerid"), nullable=False, unique=True, index=True)
	totalMemory: Mapped[float] = mapped_column(Float, unique=False, nullable=False)
	available_memory: Mapped[float] = mapped_column(Float, unique=False, nullable=False)
	usage: Mapped[float] = mapped_column(Float, unique=False, nullable=False)

class networkingInfo(Base):
	__tablename__ = "netinfo"

	computerid: Mapped[str] = mapped_column(primary_key=True, ForeignKey("computerInfo.computerid"), nullable=False, unique=True, index=True)
	ifcount: Mapped[int] = mapped_column(Integer, nullable = False, unique=False)
	ifname: Mapped[str] = mapped_column(String(200), unique=False, nullable=False)
	ipaddr: Mapped[str] = mapped_column(String(135), unique=False, nullable=False)
	

class processesInfo(Base):
	__tablename__ = "processesinfo"

	computerid: Mapped[str] = mapped_column(primary_key=True, ForeignKey("computerInfo.computerid"), nullable=False, unique=True, index=True)
	process_id: Mapped[int] = mapped_column(Integer, primary_key=True)
	processes_count: Mapped[int] = mapped_column(Integer, nullable = False, unique=False)
	pid: Mapped[int] = mapped_column(Integer, nullable = False, unique=False)
	process_name: Mapped[str] = mapped_column(String(20), unique=False, nullable=False)

class disksInfo(Base):
	__tablename__ = "disksinfo"

	computerid: Mapped[str] = mapped_column(primary_key=True, ForeignKey("computerInfo.computerid"), nullable=False, unique=True, index=True)
	processes_count: Mapped[int] = mapped_column(Integer, nullable = False, unique=False)
	partitionname: Mapped[str] = mapped_column(String(50), unique=False, nullable=False)
	mountpoint: Mapped[str] = mapped_column(String(50), unique=False, nullable=True)
	fstype: Mapped[str] = mapped_column(String(10), unique=False, nullable=False)
