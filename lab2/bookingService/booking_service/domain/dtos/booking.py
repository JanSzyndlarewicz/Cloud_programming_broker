from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, Column, Date, DateTime
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import Float, ForeignKey, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

from enum import Enum

from sqlalchemy import Column, Date
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class RoomStatus(Enum):
    available = "available"
    booked = "booked"


class BookingStatus(Enum):
    pending = "pending"
    confirmed = "confirmed"
    canceled = "canceled"


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(String(50), nullable=False, unique=True)
    price_per_night = Column(Float, nullable=False)
    status = Column(SQLEnum(RoomStatus), default=RoomStatus.available)

    # One-to-many relationship (one room can have many bookings over time)
    bookings = relationship("Booking", back_populates="room")


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    guest_name = Column(String(100), nullable=False)
    guest_email = Column(String(100), nullable=False)
    check_in = Column(Date, nullable=False)
    check_out = Column(Date, nullable=False)
    total_cost = Column(Float)
    number_of_guests = Column(Integer, nullable=False)
    status = Column(SQLEnum(BookingStatus), default=BookingStatus.pending)
    meal_reserved = Column(Boolean, default=False)  # Indicates if a meal is reserved

    # Foreign key for one room per booking
    room_id = Column(Integer, ForeignKey("rooms.id"))
    room = relationship("Room", back_populates="bookings")

    def calculate_total_cost(self):
        """Calculate cost based on room price and stay duration"""
        if not self.room:
            raise ValueError("No room assigned to booking")

        duration = (self.check_out - self.check_in).days
        if duration <= 0:
            raise ValueError("Invalid date range")

        self.total_cost = self.room.price_per_night * duration
