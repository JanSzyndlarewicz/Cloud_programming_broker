from cleaning_service.infrastructure.persistence.models import Base
from sqlalchemy import Column, Date, DateTime, Integer, String, func


class Cleaning(Base):
    __tablename__ = "cleanings"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, nullable=False)
    cleaning_date = Column(Date, nullable=False)
    cleaning_type = Column(String, nullable=False)
    assigned_staff = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
