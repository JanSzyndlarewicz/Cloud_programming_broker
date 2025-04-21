import logging
from datetime import datetime, timedelta

from dining_service.app.events.dining_created_event_publisher import DiningCreatedEventPublisher
from dining_service.domain.events.booking_created import BookingCreatedEvent
from dining_service.domain.events.dining_created import DiningCreatedEvent
from dining_service.infrastructure.database.models import DiningReservation
from dining_service.infrastructure.database.repositories import DiningReservationRepository

logger = logging.getLogger(__name__)


class BookingCreatedEventSubscriber:
    def __init__(
        self,
        dining_repository: DiningReservationRepository,
        event_publisher: DiningCreatedEventPublisher,
    ):
        self.dining_repository = dining_repository
        self.event_publisher = event_publisher

    def handle(self, event: dict):
        logger.info(f"Handling BookingCreatedEvent: {event}")
        try:
            # Convert dictionary to BookingCreatedEvent
            logger.info(f"Converting event to BookingCreatedEvent: {event}")
            event_obj = BookingCreatedEvent(**event)
            logger.info(f"Converted event: {event_obj.model_dump()}")

            if not event_obj.meal_reserved:
                return

            reservation_start_date = datetime.strptime(event_obj.check_in, "%Y-%m-%d").date()
            reservation_end_date = datetime.strptime(event_obj.check_out, "%Y-%m-%d").date()

            current_date = reservation_start_date
            while current_date <= reservation_end_date:
                reservation = DiningReservation(
                    guest_name=event_obj.guest_name,
                    guest_email=event_obj.guest_email,
                    reservation_date=current_date,
                    number_of_guests=event_obj.number_of_guests,
                )
                self.dining_repository.session.add(reservation)
                self.dining_repository.session.commit()  # Commit to generate the ID

                dining_event = DiningCreatedEvent(
                    dining_id=reservation.id,  # ID is now available
                    guest_name=reservation.guest_name,
                    guest_email=reservation.guest_email,
                    reservation_date=reservation.reservation_date.isoformat(),
                    number_of_guests=reservation.number_of_guests,
                )
                self.event_publisher.publish(dining_event)

                current_date += timedelta(days=1)

        except Exception as e:
            logger.error(f"Failed to handle BookingCreatedEvent: {str(e)}")
            self.dining_repository.session.rollback()
            raise
