import enum

from booking_service.infrastructure.persistence.models import Base
from sqlalchemy import Column, DateTime, Enum, Float, Integer, String, func
from sqlalchemy.orm import relationship


class RoomStatus(enum.Enum):
    available = "available"
    booked = "booked"
    maintenance = "maintenance"


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(String, nullable=False)
    price_per_night = Column(Float, nullable=False)
    status = Column(Enum(RoomStatus), default=RoomStatus.available, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    # Odwołanie do klasy Booking jako ciąg znaków
    bookings = relationship("Booking", back_populates="room")
