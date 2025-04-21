from sqlalchemy.orm import declarative_base

Base = declarative_base()

from sqlalchemy import Column, Date, Time
from sqlalchemy import Integer, String


class DiningReservation(Base):
    __tablename__ = "dining_reservations"

    id = Column(Integer, primary_key=True, index=True)
    guest_name = Column(String(100), nullable=False)
    guest_email = Column(String(100), nullable=False)
    reservation_date = Column(Date, nullable=False)  # Date of the reservation
    number_of_guests = Column(Integer, nullable=False)  # Number of guests
