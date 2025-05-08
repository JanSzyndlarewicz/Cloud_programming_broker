import logging
from datetime import datetime

from app.events.cleaning_created_event_publisher import CleaningCreatedEventPublisher
from domain.dtos.cleaning import Cleaning, RoomStatus
from domain.events.booking_created import BookingCreatedEvent
from domain.events.cleaning_created import CleaningCreatedEvent
from infrastructure.persistence.repositories.cleaning_repository import (
    CleaningRepository,
    RoomRepository,
)

logger = logging.getLogger(__name__)


class BookingCreatedEventSubscriber:
    def __init__(
        self,
        cleaning_repository: CleaningRepository,
        room_repository: RoomRepository,
        event_publisher: CleaningCreatedEventPublisher,
    ):
        self.cleaning_repository = cleaning_repository
        self.room_repository = room_repository
        self.event_publisher = event_publisher

    def handle(self, event: dict):
        logger.info(f"Handling BookingCreatedEvent: {event}")
        try:
            # Convert dictionary to BookingCreatedEvent
            logger.info(f"Converting event to BookingCreatedEvent: {event}")
            event_obj = BookingCreatedEvent(**event)
            logger.info(f"Converted event: {event_obj.model_dump()}")
            print(event_obj.model_dump())

            # Get the room associated with the booking
            room = self.room_repository.get_room_by_id(event_obj.room_id)
            if not room:
                raise ValueError(f"Room {event_obj.room_id} not found")

            # Create a cleaning task
            cleaning_date = datetime.strptime(event_obj.check_out, "%Y-%m-%d").date()
            cleaning = Cleaning(
                room_id=event_obj.room_id,
                cleaning_date=cleaning_date,
                cleaning_type="standard",
                assigned_staff="auto-assigned",
            )

            # Update room status to cleaning
            room.status = RoomStatus.cleaning.value

            # Save cleaning task and update room status
            self.cleaning_repository.session.add(cleaning)
            self.cleaning_repository.session.add(room)
            self.cleaning_repository.session.commit()
            self.cleaning_repository.session.refresh(cleaning)

            # Publish cleaning_created event
            cleaning_event = CleaningCreatedEvent(
                cleaning_id=cleaning.id,
                room_id=cleaning.room_id,
                room_number=event_obj.room_number,  # Include room_number
                cleaning_date=cleaning.cleaning_date.isoformat(),
                cleaning_type=cleaning.cleaning_type,
                assigned_staff=cleaning.assigned_staff,
            )
            self.event_publisher.publish(cleaning_event)

        except Exception as e:
            logger.error(f"Failed to handle BookingCreatedEvent: {str(e)}")
            self.cleaning_repository.session.rollback()
            raise
