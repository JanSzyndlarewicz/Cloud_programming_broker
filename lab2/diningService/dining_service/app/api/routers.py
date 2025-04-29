from dining_service.app.api.controllers import DiningController
from dining_service.app.commands.create_dining_command_handler import CreateDiningCommandHandler
from dining_service.app.events.dining_created_event_publisher import DiningCreatedEventPublisher
from dining_service.app.queries.get_dining_reservations_query_handler import GetDiningReservationsQueryHandler
from dining_service.infrastructure.messaging.event_bus import RabbitMQEventBus
from dining_service.infrastructure.persistence import get_db
from dining_service.infrastructure.persistence.repositories.dining_reservation_repository import (
    DiningReservationRepository,
)
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()


def get_dining_controller(db: Session = Depends(get_db)):
    dining_repository = DiningReservationRepository(db)
    event_bus = RabbitMQEventBus()
    event_publisher = DiningCreatedEventPublisher(event_bus)
    create_dining_command_handler = CreateDiningCommandHandler(
        dining_repository,
        event_publisher,
    )
    return DiningController(create_dining_command_handler, GetDiningReservationsQueryHandler(dining_repository))


@router.get("/dining-reservations")
async def list_dining_reservations(controller: DiningController = Depends(get_dining_controller)):
    return await controller.get_dining_reservations()
