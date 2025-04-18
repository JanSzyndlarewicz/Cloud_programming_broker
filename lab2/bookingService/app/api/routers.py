from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.controllers import BookingController, RoomController
from app.commands.create_booking_command import CreateBookingCommand
from app.commands.create_booking_command_handler import CreateBookingCommandHandler
from app.events.booking_created_event import BookingCreatedEventPublisher
from app.query.get_booking_query_handler import GetBookingQueryHandler
from app.query.get_bookings_query_handler import GetBookingsQueryHandler
from app.query.get_rooms_query_handler import GetRoomsQueryHandler
from infrastructure.database.init import get_db
from infrastructure.database.repositories import BookingRepository, RoomRepository
from infrastructure.event_bus.rabbitmq_event_bus import RabbitMQEventBus

router = APIRouter()


def get_booking_controller(db: Session = Depends(get_db)):
    event_bus = RabbitMQEventBus()
    booking_repository = BookingRepository(db)
    room_repository = RoomRepository(db)
    event_publisher = BookingCreatedEventPublisher(event_bus)
    return BookingController(
        CreateBookingCommandHandler(booking_repository, room_repository, event_publisher),
        GetBookingsQueryHandler(booking_repository),
        GetBookingQueryHandler(booking_repository),
    )

def get_room_controller(db: Session = Depends(get_db)):
    room_repository = RoomRepository(db)
    return RoomController(GetRoomsQueryHandler(room_repository))



def get_booking_repository(db: Session = Depends(get_db)):
    return BookingRepository(db)


from pydantic import BaseModel, EmailStr


class Room(BaseModel):
    room_id: int
    nights: int

class CreateBookingRequest(BaseModel):
    guest_name: str
    guest_email: EmailStr
    room: Room
    check_in: str
    check_out: str

@router.post("/bookings")
async def create_booking(
    booking_request: CreateBookingRequest,
    controller: BookingController = Depends(get_booking_controller),
):

    command = CreateBookingCommand(
        guest_name=booking_request.guest_name,
        guest_email=booking_request.guest_email,
        room=booking_request.room.model_dump(),
        check_in=booking_request.check_in,
        check_out=booking_request.check_out,
    )
    return await controller.create_booking(command)


@router.get("/bookings")
async def list_bookings(controller: BookingController = Depends(get_booking_controller)):
    return await controller.get_bookings()


@router.get("/bookings/{booking_id}")
async def get_booking(booking_id: int, controller: BookingController = Depends(get_booking_controller)):
    return await controller.get_booking(booking_id)

@router.get("/rooms")
async def list_rooms(controller: RoomController = Depends(get_room_controller)):
    return await controller.get_rooms()