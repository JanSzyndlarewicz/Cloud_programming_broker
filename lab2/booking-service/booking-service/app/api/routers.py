from app.api.controllers import BookingController, RoomController
from app.commands.create_booking_command import CreateBookingCommand
from app.commands.create_booking_command_handler import CreateBookingCommandHandler
from app.dtos.booking import CreateBookingRequest
from app.events.booking_created_event import BookingCreatedEventPublisher
from app.queries.get_booking_query_handler import GetBookingQueryHandler
from app.queries.get_bookings_query_handler import GetBookingsQueryHandler
from app.queries.get_rooms_query_handler import GetRoomsQueryHandler
from infrastructure.messaging.event_bus import RabbitMQEventBus
from infrastructure.persistence import get_db
from infrastructure.persistence.repositories.booking_repository import BookingRepository
from infrastructure.persistence.repositories.room_repository import RoomRepository
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

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


@router.post("/bookings")
async def create_booking(
    booking_request: CreateBookingRequest,
    controller: BookingController = Depends(get_booking_controller),
):
    return await controller.create_booking(booking_request)


@router.get("/bookings")
async def list_bookings(controller: BookingController = Depends(get_booking_controller)):
    return await controller.get_bookings()


@router.get("/bookings/{booking_id}")
async def get_booking(booking_id: int, controller: BookingController = Depends(get_booking_controller)):
    return await controller.get_booking(booking_id)


@router.get("/rooms")
async def list_rooms(controller: RoomController = Depends(get_room_controller)):
    return await controller.get_rooms()
