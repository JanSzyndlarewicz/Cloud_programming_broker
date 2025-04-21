from cleaning_service.app.commands.create_cleaning_command import CreateCleaningCommand
from cleaning_service.app.commands.create_cleaning_command_handler import CreateCleaningCommandHandler
from cleaning_service.app.query.get_rooms_query_handler import GetRoomsQueryHandler
from fastapi import HTTPException


class CleaningController:
    def __init__(
        self,
        create_cleaning_command_handler: CreateCleaningCommandHandler,
    ):
        self.create_cleaning_command_handler = create_cleaning_command_handler

    async def create_cleaning(self, command: CreateCleaningCommand) -> dict:
        try:
            cleaning_id = self.create_cleaning_command_handler.handle(command)
            return {"cleaning_id": cleaning_id, "status": "created"}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))


class RoomController:
    def __init__(self, get_rooms_query_handler: GetRoomsQueryHandler):
        self.get_rooms_query_handler = get_rooms_query_handler

    async def get_rooms(self):
        return self.get_rooms_query_handler.handle()
