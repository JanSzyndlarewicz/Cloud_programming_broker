from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.orm import relationship

from app.infrastructure.database import Base


class FlightPreferences(Base):
    __tablename__ = "flight_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    destination = Column(String, index=True)
    departure_date = Column(Date)
    return_date = Column(Date)
    max_price = Column(Float)
    flight_class = Column(String)
    airlines = Column(String)

    user = relationship("User", back_populates="preferences")

