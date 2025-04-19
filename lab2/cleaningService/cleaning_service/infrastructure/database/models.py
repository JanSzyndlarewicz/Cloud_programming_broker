import enum

from sqlalchemy import Column, Date, DateTime, Enum, Integer, String, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class RoomStatus(enum.Enum):
    available = "available"
    cleaning = "cleaning"
    maintenance = "maintenance"


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(String, nullable=False, unique=True)
    status = Column(Enum(RoomStatus), default=RoomStatus.available, nullable=False)
    created_at = Column(DateTime, server_default=func.now())


class Cleaning(Base):
    __tablename__ = "cleanings"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, nullable=False)
    cleaning_date = Column(Date, nullable=False)
    cleaning_type = Column(String, nullable=False)
    assigned_staff = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())