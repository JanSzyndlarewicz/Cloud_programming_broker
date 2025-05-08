from sqlalchemy.orm import declarative_base

Base = declarative_base()

from infrastructure.persistence.models.orm_cleaning import Cleaning
from infrastructure.persistence.models.orm_room import Room
