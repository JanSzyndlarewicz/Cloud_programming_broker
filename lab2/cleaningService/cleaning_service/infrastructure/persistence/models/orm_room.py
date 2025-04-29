import enum

from sqlalchemy import Column, DateTime, Enum, Integer, String, func

from cleaning_service.infrastructure.persistence.models import Base


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
