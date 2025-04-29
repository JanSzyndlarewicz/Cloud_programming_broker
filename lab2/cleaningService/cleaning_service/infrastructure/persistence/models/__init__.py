from sqlalchemy.orm import declarative_base

Base = declarative_base()

from cleaning_service.infrastructure.persistence.models.orm_room import Room
from cleaning_service.infrastructure.persistence.models.orm_cleaning import Cleaning