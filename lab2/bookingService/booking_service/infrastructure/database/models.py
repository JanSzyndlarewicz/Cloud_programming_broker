import enum

from sqlalchemy import Column, Date, DateTime, Enum, Float, ForeignKey, Integer, String, func, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class BookingStatus(enum.Enum):  # Ensure this is a proper enum.Enum
    pending = "pending"
    confirmed = "confirmed"
    canceled = "canceled"


class RoomStatus(enum.Enum):
    available = "available"
    booked = "booked"
    maintenance = "maintenance"


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(String, nullable=False)
    price_per_night = Column(Float, nullable=False)
    status = Column(Enum(RoomStatus), default=RoomStatus.available, nullable=False)  # Correct usage
    created_at = Column(DateTime, server_default=func.now())

    bookings = relationship("Booking", back_populates="room")


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    guest_name = Column(String, nullable=False)
    guest_email = Column(String, nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    check_in = Column(Date, nullable=False)
    check_out = Column(Date, nullable=False)
    total_cost = Column(Float, nullable=False)
    number_of_guests = Column(Integer, nullable=False)
    status = Column(Enum(BookingStatus), default=BookingStatus.pending, nullable=False)
    meal_reserved = Column(Boolean, default=False, nullable=False)  # Indicates if a meal is reserved
    created_at = Column(DateTime, server_default=func.now())

    room = relationship("Room", back_populates="bookings")
