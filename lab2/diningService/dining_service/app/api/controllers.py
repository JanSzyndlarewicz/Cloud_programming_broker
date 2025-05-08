from typing import Optional

from app.commands.create_dining_command import CreateDiningCommand
from app.commands.create_dining_command_handler import CreateDiningCommandHandler
from app.queries.get_dining_reservations_query_handler import GetDiningReservationsQueryHandler
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

    async def get_dining_reservations(self, guest_name: Optional[str] = None, reservation_date: Optional[str] = None,
                                      guest_email: Optional[str] = None):
        try:
            return self.get_dining_reservations_query_handler.handle(
                guest_name=guest_name,
                reservation_date=reservation_date,
                guest_email=guest_email
            )
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
