from typing import Type

from cleaning_service.infrastructure.persistence.models.orm_cleaning import Cleaning
from cleaning_service.infrastructure.persistence.models.orm_room import Room
from sqlalchemy.orm import Session


class CleaningRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, cleaning: Cleaning) -> Cleaning:
        db_cleaning = Cleaning(
            room_id=cleaning.room_id,
            cleaning_date=cleaning.cleaning_date,
            cleaning_type=cleaning.cleaning_type,
            assigned_staff=cleaning.assigned_staff,
        )
        self.session.add(db_cleaning)
        self.session.commit()
        self.session.refresh(db_cleaning)
        return db_cleaning

    def get(self, cleaning_id: int) -> Cleaning | None:
        return self.session.query(Cleaning).filter(Cleaning.id == cleaning_id).first()

    def list_all(self) -> list[Type[Cleaning]]:
        return self.session.query(Cleaning).all()


class RoomRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_all_rooms(self):
        return self.db_session.query(Room).all()

    def get_room_by_id(self, room_id: int) -> Room | None:
        return self.db_session.query(Room).filter(Room.id == room_id).first()

    def update_room_status(self, room_id: int, status: str) -> None:
        room = self.get_room_by_id(room_id)
        if room:
            room.status = status
            self.db_session.commit()
