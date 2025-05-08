from app.events.booking_created_event_subscriber import BookingCreatedEventSubscriber
from app.events.dining_created_event_publisher import DiningCreatedEventPublisher
from infrastructure.messaging.event_bus import RabbitMQEventBus
from infrastructure.persistence.repositories.dining_reservation_repository import (
    DiningReservationRepository,
)
from sqlalchemy.orm import Session


def setup_event_subscribers(db: Session, event_bus: RabbitMQEventBus):
    dining_repository = DiningReservationRepository(db)
    event_publisher = DiningCreatedEventPublisher(event_bus)

    booking_created_subscriber = BookingCreatedEventSubscriber(dining_repository, event_publisher)

    # Subscribe to the "booking_created" event type
    event_bus.start_subscription_in_thread(
        queue=f"dining_room_booked_queue", callback=booking_created_subscriber.handle, exchange_type="fanout"
    )
