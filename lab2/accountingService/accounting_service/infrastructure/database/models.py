from sqlalchemy import Column, Date, DateTime, Integer, String, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class DiningReservation(Base):
    __tablename__ = "dining_reservations"

    id = Column(Integer, primary_key=True, index=True)
    guest_name = Column(String, nullable=False)
    guest_email = Column(String, nullable=False)
    reservation_date = Column(Date, nullable=False)  # Date of the reservation
    number_of_guests = Column(Integer, nullable=False)  # Number of guests
    created_at = Column(DateTime, server_default=func.now())
