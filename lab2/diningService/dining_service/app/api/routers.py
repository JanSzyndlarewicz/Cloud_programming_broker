from typing import Optional

from app.api.controllers import DiningController
from app.commands.create_dining_command_handler import CreateDiningCommandHandler
from app.events.dining_created_event_publisher import DiningCreatedEventPublisher
from app.queries.get_dining_reservations_query_handler import GetDiningReservationsQueryHandler
from infrastructure.messaging.event_bus import RabbitMQEventBus
from infrastructure.persistence import get_db
from infrastructure.persistence.repositories.dining_reservation_repository import (
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
async def list_dining_reservations(
    controller: DiningController = Depends(get_dining_controller),
    guest_name: Optional[str] = None,
    reservation_date: Optional[str] = None,
    guest_email: Optional[str] = None,
):
    return await controller.get_dining_reservations(
        guest_name=guest_name,
        reservation_date=reservation_date,
        guest_email=guest_email
    )
