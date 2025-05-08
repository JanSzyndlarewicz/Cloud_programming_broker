import logging
from datetime import datetime
from typing import Optional

from app.commands.create_dining_command import CreateDiningCommand
from app.events.dining_created_event_publisher import DiningCreatedEventPublisher
from domain.events.dining_created import DiningCreatedEvent
from infrastructure.persistence.models.orm_dining_reservation import DiningReservation
from infrastructure.persistence.repositories.dining_reservation_repository import (
    DiningReservationRepository,
)

logger = logging.getLogger(__name__)


class CreateDiningCommandHandler:
    def __init__(
        self,
        dining_repository: DiningReservationRepository,
        event_publisher: DiningCreatedEventPublisher,
    ):
        self.dining_repository = dining_repository
        self.event_publisher = event_publisher

    def handle(self, command: CreateDiningCommand) -> Optional[int]:
        try:
            # Convert and validate reservation date and time
            reservation_date = datetime.strptime(command.reservation_start_date, "%Y-%m-%d").date()

            # Create dining reservation
            reservation = DiningReservation(
                guest_name=command.guest_name,
                guest_email=command.guest_email,
                reservation_date=reservation_date,
                number_of_guests=command.number_of_guests,
            )

            # Save reservation
            self.dining_repository.session.add(reservation)
            self.dining_repository.session.commit()
            self.dining_repository.session.refresh(reservation)

            # Publish event
            event = DiningCreatedEvent(
                dining_id=reservation.id,
                guest_name=reservation.guest_name,
                guest_email=reservation.guest_email,
                reservation_date=reservation.reservation_date.isoformat(),
                number_of_guests=reservation.number_of_guests,
            )
            self.event_publisher.publish(event)

            return reservation.id

        except Exception as e:
            logger.info(f"Dining reservation creation failed: {str(e)}")
            self.dining_repository.session.rollback()
            raise
