from sqlalchemy import Boolean, Column, Date, DateTime, Enum, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship
from booking_service.infrastructure.persistence.models import Base
import enum


class BookingStatus(enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    canceled = "canceled"


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
    meal_reserved = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    # Odwołanie do klasy Room jako ciąg znaków
    room = relationship("Room", back_populates="bookings")