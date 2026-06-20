from __future__ import annotations
from datetime import timezone, datetime

from sqlalchemy import DateTime, ForeignKey, Integer, Float, String, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db import Base, engine

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
	severity Mapped[str] = mapped_column(String(15), unique=False, nullable=True)
	computers = relationship("ComputerInfo", back_populates="location")

class ComputerInfo(Base):
	__tablename__ = "computerInfo"

	computer_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
	computername: Mapped[str] = mapped_column(String(50), unique=False, nullable=False)
	is_unix: Mapped[bool] = mapped_column(Boolean, unique=False, nullable=False)
	os: Mapped[str] = mapped_column(String(50), unique=False, nullable=True)  ## TODO : Fix this (nullable=False)
	boottime: Mapped[datetime] = mapped_column(DateTime, unique = False, nullable=False)
	node_machineid: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
	fingerprint: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
	added_on: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now())
	last_heartbeat: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now())
	is_alive: Mapped[bool] = mapped_column(Boolean, unique=False, nullable=False)

	# Relationships
	location_id = mapped_column(
        ForeignKey("locations.id"), nullable = True, default=None
    )
	location = relationship("Locations", back_populates="computers")
	processes = relationship("processesInfo", back_populates="computer")
	memoryinfo = relationship("MemoryInfo", back_populates="computer")
	netinfo = relationship("networkingInfo", back_populates="computer")
	disksinfo = relationship("disksInfo", back_populates="computer")
	computerusers = relationship("computerUsers", back_populates="computer")
	usb_devices = relationship("usbInfo", back_populates="computer")
	keys = relationship("Keys", back_populates="computer")


class MemoryInfo(Base):
	__tablename__ = "memoryinfo"

	computer_id = mapped_column(
        ForeignKey("computerInfo.computer_id")
    )
	entryid: Mapped[int] = mapped_column(Integer, primary_key=True)
	computer: Mapped[ComputerInfo] = relationship("ComputerInfo",back_populates="memoryinfo")
	totalMemory: Mapped[float] = mapped_column(Float, unique=False, nullable=False)
	available_memory: Mapped[float] = mapped_column(Float, unique=False, nullable=False)
	usage: Mapped[float] = mapped_column(Float, unique=False, nullable=False)

class networkingInfo(Base):
	__tablename__ = "netinfo"

	computer_id = mapped_column(
        ForeignKey("computerInfo.computer_id")
    )
	computer: Mapped[ComputerInfo] = relationship("ComputerInfo", back_populates="netinfo")
	if_id: Mapped[int] = mapped_column(Integer, primary_key=True)
	ifname: Mapped[str] = mapped_column(String(200), unique=False, nullable=False)
	ipaddr: Mapped[str] = mapped_column(String(135), unique=False, nullable=True)
	

class processesInfo(Base):
	__tablename__ = "processesinfo"

	computer_id = mapped_column(
        ForeignKey("computerInfo.computer_id")
    )
	computer: Mapped[ComputerInfo] = relationship("ComputerInfo",back_populates="processes")
	process_id: Mapped[int] = mapped_column(Integer, primary_key=True)
	pid: Mapped[int] = mapped_column(Integer, nullable = True, unique=False)
	username: Mapped[str] = mapped_column(String(200), unique=False, nullable=True)
	name: Mapped[str] = mapped_column(String(20), unique=False, nullable=True)

class disksInfo(Base):
	__tablename__ = "disksinfo"

	computer_id = mapped_column(
        ForeignKey("computerInfo.computer_id")
    )
	computer: Mapped[ComputerInfo] = relationship("ComputerInfo",back_populates="disksinfo")
	disk_id: Mapped[int] = mapped_column(Integer, primary_key=True)
	partitionname: Mapped[str] = mapped_column(String(50), unique=False, nullable=False)
	mountpoint: Mapped[str] = mapped_column(String(50), unique=False, nullable=True)
	fstype: Mapped[str] = mapped_column(String(10), unique=False, nullable=False)

class computerUsers(Base):
	__tablename__ = "computerusers"

	computer_id = mapped_column(
        ForeignKey("computerInfo.computer_id")
    )
	userid: Mapped[int] = mapped_column(Integer, primary_key=True)
	computer: Mapped[ComputerInfo] = relationship("ComputerInfo",back_populates="computerusers")
	username: Mapped[str] = mapped_column(String(200), unique=False, nullable=False)

class usbInfo(Base):
	__tablename__ = "usb_devices"
	computer_id = mapped_column(
        ForeignKey("computerInfo.computer_id")
    )
	computer: Mapped[ComputerInfo] = relationship("ComputerInfo",back_populates="usb_devices")
	device_id: Mapped[int] = mapped_column(Integer, primary_key=True)
	manufacturer: Mapped[str] = mapped_column(String(50), unique=False, nullable=True)
	product: Mapped[str] = mapped_column(String(50), unique=False, nullable=True)
	vendor_id: Mapped[str] = mapped_column(String(200), unique=False, nullable=False)
	product_id: Mapped[str] = mapped_column(String(200), unique=False, nullable=False)

class Keys(Base):
	__tablename__ = "keys"
	computer_id = mapped_column(
			ForeignKey("computerInfo.computer_id")
	)
	key_id: Mapped[int] = mapped_column(Integer, primary_key=True)
	computer: Mapped[ComputerInfo] = relationship("ComputerInfo",back_populates="keys")
	key: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
	length: Mapped[int] = mapped_column(Integer)