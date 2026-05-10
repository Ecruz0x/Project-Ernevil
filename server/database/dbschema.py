from __future__ import annotations
from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, Integer, Float, String, Text, Boolean, 
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base

Base.metadata.create_all(bind=engine)

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

	computerid: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
	computername: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
	is_unix: Mapped[bool] = mapped_column(Boolean, unique=False, nullable=False)
	location: Mapped[int] = relationship(back_populates="computerInfo", nullable=True)
	os: Mapped[str] = mapped_column(String(50), unique=False, nullable=True)  ## TODO : Fix this (nullable=False)
	boottime: Mapped[datetime] = mapped_column(DateTime, unique = False, nullable=False)
	is_alive: Mapped[bool] = mapped_column(Boolean, unique=False, nullable=False)
	node_machineid: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
	uuid: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
	added_on: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
	fingerprint: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)


class MemoryInfo(Base):
	__tablename__ = "memoryinfo"

	entryid: Mapped[int] = mapped_column(Integer, primary_key=True)
	computer: Mapped[ComputerInfo] = relationship(back_populates="memoryinfo")
	totalMemory: Mapped[float] = mapped_column(Float, unique=False, nullable=False)
	available_memory: Mapped[float] = mapped_column(Float, unique=False, nullable=False)
	usage: Mapped[float] = mapped_column(Float, unique=False, nullable=False)

class networkingInfo(Base):
	__tablename__ = "netinfo"

	computer: Mapped[ComputerInfo] = relationship(back_populates="netinfo")
	if_id: Mapped[int] = mapped_column(Integer, primary_key=True)
	ifname: Mapped[str] = mapped_column(String(200), unique=False, nullable=False)
	ipaddr: Mapped[str] = mapped_column(String(135), unique=False, nullable=False)
	

class processesInfo(Base):
	__tablename__ = "processesinfo"

	computer: Mapped[ComputerInfo] = relationship(back_populates="processesinfo")
	process_id: Mapped[int] = mapped_column(Integer, primary_key=True)
	pid: Mapped[int] = mapped_column(Integer, nullable = False, unique=False)
	user: Mapped[str] = mapped_column(String(200), unique=False, nullable=False)
	process_name: Mapped[str] = mapped_column(String(20), unique=False, nullable=False)

class disksInfo(Base):
	__tablename__ = "disksinfo"

	computer: Mapped[ComputerInfo] = relationship(back_populates="disksinfo")
	disk_id: Mapped[int] = mapped_column(Integer, primary_key=True)
	partitionname: Mapped[str] = mapped_column(String(50), unique=False, nullable=False)
	mountpoint: Mapped[str] = mapped_column(String(50), unique=False, nullable=True)
	fstype: Mapped[str] = mapped_column(String(10), unique=False, nullable=False)

class HBRInfo(Base):
	__tablename__ = "heartbeatsRef"

	computer: Mapped[ComputerInfo] = relationship(back_populates="heartbeats")
	HBID: Mapped[int] = mapped_column(Integer, primary_key=True)
	lastHB: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
	last_refresh Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
