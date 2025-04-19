from cleaning_service.app.api.controllers import CleaningController, RoomController
from cleaning_service.app.commands.create_cleaning_command import CreateCleaningCommand
from cleaning_service.app.commands.create_cleaning_command_handler import CreateCleaningCommandHandler
from cleaning_service.app.query.get_rooms_query_handler import GetRoomsQueryHandler
from fastapi import APIRouter, Depends
from cleaning_service.infrastructure.database.init import get_db
from cleaning_service.infrastructure.database.repositories import CleaningRepository, RoomRepository
from cleaning_service.infrastructure.event_bus.rabbitmq_event_bus import RabbitMQEventBus
from sqlalchemy.orm import Session

router = APIRouter()


def get_cleaning_controller(db: Session = Depends(get_db)):
    event_bus = RabbitMQEventBus()
    cleaning_repository = CleaningRepository(db)
    room_repository = RoomRepository(db)
    return CleaningController(
        CreateCleaningCommandHandler(cleaning_repository, room_repository, event_bus)
    )


def get_room_controller(db: Session = Depends(get_db)):
    room_repository = RoomRepository(db)
    return RoomController(GetRoomsQueryHandler(room_repository))


from pydantic import BaseModel


class CreateCleaningRequest(BaseModel):
    room_id: int
    cleaning_date: str
    cleaning_type: str
    assigned_staff: str


@router.post("/cleanings")
async def create_cleaning(
    cleaning_request: CreateCleaningRequest,
    controller: CleaningController = Depends(get_cleaning_controller),
):
    command = CreateCleaningCommand(
        room_id=cleaning_request.room_id,
        cleaning_date=cleaning_request.cleaning_date,
        cleaning_type=cleaning_request.cleaning_type,
        assigned_staff=cleaning_request.assigned_staff,
    )
    return await controller.create_cleaning(command)


@router.get("/rooms")
async def list_rooms(controller: RoomController = Depends(get_room_controller)):
    return await controller.get_rooms()