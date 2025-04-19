from cleaning_service.infrastructure.database.repositories import RoomRepository


class GetRoomsQueryHandler:
    def __init__(self, room_repository: RoomRepository):
        self.room_repository = room_repository

    def handle(self) -> list:
        return self.room_repository.get_all_rooms()
