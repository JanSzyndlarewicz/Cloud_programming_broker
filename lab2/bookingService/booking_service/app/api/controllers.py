from app.commands.create_booking_command import CreateBookingCommand
from app.commands.create_booking_command_handler import CreateBookingCommandHandler
from app.dtos.booking import CreateBookingRequest
from app.queries.get_booking_query_handler import GetBookingQueryHandler
from app.queries.get_bookings_query_handler import GetBookingsQueryHandler
from app.queries.get_rooms_query_handler import GetRoomsQueryHandler
from fastapi import HTTPException


class BookingController:
    def __init__(
        self,
        create_booking_command_handler: CreateBookingCommandHandler,
        get_bookings_query_handler: GetBookingsQueryHandler,
        get_booking_query_handler: GetBookingQueryHandler,
    ):
        self.create_booking_command_handler = create_booking_command_handler
        self.get_bookings_query_handler = get_bookings_query_handler
        self.get_booking_query_handler = get_booking_query_handler

    async def create_booking(self, booking_request: CreateBookingRequest) -> dict:
        try:
            command = CreateBookingCommand(
                guest_name=booking_request.guest_name,
                guest_email=booking_request.guest_email,
                room=booking_request.room.model_dump(),
                check_in=booking_request.check_in,
                check_out=booking_request.check_out,
                number_of_guests=booking_request.number_of_guests,
                meal_reserved=booking_request.meal_reserved,
            )
            booking_id = self.create_booking_command_handler.handle(command)
            return {"booking_id": booking_id, "status": "created"}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def get_bookings(self):
        return self.get_bookings_query_handler.handle()

    async def get_booking(self, booking_id: int):
        return self.get_booking_query_handler.handle(booking_id)


class RoomController:
    def __init__(self, get_rooms_query_handler: GetRoomsQueryHandler):
        self.get_rooms_query_handler = get_rooms_query_handler

    async def get_rooms(self):
        return self.get_rooms_query_handler.handle()
