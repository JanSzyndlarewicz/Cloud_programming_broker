from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from enum import Enum

from sqlalchemy import Column, Date
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import Integer, String


class RoomStatus(Enum):
    available = "available"
    cleaning = "cleaning"


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(String(50), nullable=False, unique=True)
    status = Column(SQLEnum(RoomStatus), default=RoomStatus.available)


class Cleaning(Base):
    __tablename__ = "cleanings"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, nullable=False)
    cleaning_date = Column(Date, nullable=False)
    cleaning_type = Column(String(50), nullable=False)
    assigned_staff = Column(String(100), nullable=False)
