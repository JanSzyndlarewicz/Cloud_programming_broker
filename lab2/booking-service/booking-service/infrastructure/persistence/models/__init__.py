from sqlalchemy.orm import declarative_base

Base = declarative_base()

from infrastructure.persistence.models.orm_booking import Booking

# Import modeli, aby SQLAlchemy mogło je zarejestrować
from infrastructure.persistence.models.orm_room import Room
