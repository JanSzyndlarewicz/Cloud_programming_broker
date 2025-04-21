import logging
from datetime import datetime
from typing import Optional

from cleaning_service.app.commands.create_cleaning_command import CreateCleaningCommand
from cleaning_service.app.events.cleaning_created_event_publisher import CleaningCreatedEventPublisher
from cleaning_service.domain.events.cleaning_created import CleaningCreatedEvent
from cleaning_service.infrastructure.database.models import Cleaning, RoomStatus
from cleaning_service.infrastructure.database.repositories import CleaningRepository, RoomRepository

logger = logging.getLogger(__name__)


class CreateCleaningCommandHandler:
    def __init__(
        self,
        cleaning_repository: CleaningRepository,
        room_repository: RoomRepository,
        event_publisher: CleaningCreatedEventPublisher,
    ):
        self.cleaning_repository = cleaning_repository
        self.room_repository = room_repository
        self.event_publisher = event_publisher

    def handle(self, command: CreateCleaningCommand) -> Optional[int]:
        try:
            # Convert and validate cleaning date
            cleaning_date = datetime.strptime(command.cleaning_date, "%Y-%m-%d").date()

            # Get the room
            room = self.room_repository.get_room_by_id(command.room_id)
            if not room:
                raise ValueError(f"Room {command.room_id} not found")

            # Check room status
            if room.status.value != RoomStatus.available.value:
                raise ValueError(f"Room {room.number} is not available for cleaning")

            # Create cleaning task
            cleaning = Cleaning(
                room_id=command.room_id,
                cleaning_date=cleaning_date,
                cleaning_type=command.cleaning_type,
                assigned_staff=command.assigned_staff,
            )

            # Update room status
            room.status = RoomStatus.cleaning.value

            # Save changes
            self.cleaning_repository.session.add(cleaning)
            self.cleaning_repository.session.add(room)  # Explicitly add room to session
            self.cleaning_repository.session.commit()
            self.cleaning_repository.session.refresh(cleaning)

            # Publish event
            event = CleaningCreatedEvent(
                cleaning_id=cleaning.id,
                room_id=cleaning.room_id,
                cleaning_date=cleaning.cleaning_date.isoformat(),
                cleaning_type=cleaning.cleaning_type,
                assigned_staff=cleaning.assigned_staff,
            )
            self.event_publisher.publish(event)

            return cleaning.id

        except Exception as e:
            logger.info(f"Cleaning task creation failed: {str(e)}")
            self.cleaning_repository.session.rollback()
            raise
