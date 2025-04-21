from dining_service.app.commands.create_dining_command import CreateDiningCommand
from dining_service.app.commands.create_dining_command_handler import CreateDiningCommandHandler
from dining_service.app.query.get_dining_reservations_query_handler import GetDiningReservationsQueryHandler
from fastapi import HTTPException


class DiningController:
    def __init__(
        self,
        create_dining_command_handler: CreateDiningCommandHandler,
        get_dining_reservations_query_handler: GetDiningReservationsQueryHandler,
    ):
        self.create_dining_command_handler = create_dining_command_handler
        self.get_dining_reservations_query_handler = get_dining_reservations_query_handler

    async def create_dining_reservation(self, command: CreateDiningCommand) -> dict:
        try:
            reservation_id = self.create_dining_command_handler.handle(command)
            return {"reservation_id": reservation_id, "status": "created"}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def get_dining_reservations(self):
        try:
            return self.get_dining_reservations_query_handler.handle()
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))