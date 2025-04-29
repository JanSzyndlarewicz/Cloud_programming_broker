from sqlalchemy.orm import Session

from booking_service.domain.models.booking import Room


class RoomRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_all_rooms(self):
        return self.db_session.query(Room).all()

    def get_room_by_id(self, room_id: int) -> Room | None:
        return self.db_session.query(Room).filter(Room.id == room_id).first()