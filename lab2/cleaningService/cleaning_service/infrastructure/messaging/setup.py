from app.events.booking_created_event_subscriber import BookingCreatedEventSubscriber
from app.events.cleaning_created_event_publisher import CleaningCreatedEventPublisher
from infrastructure.messaging.event_bus import RabbitMQEventBus
from infrastructure.persistence.repositories.cleaning_repository import (
    CleaningRepository,
    RoomRepository,
)
from sqlalchemy.orm import Session


def setup_event_subscribers(db: Session, event_bus: RabbitMQEventBus):
    cleaning_repository = CleaningRepository(db)
    room_repository = RoomRepository(db)
    event_publisher = CleaningCreatedEventPublisher(event_bus)

    booking_created_subscriber = BookingCreatedEventSubscriber(cleaning_repository, room_repository, event_publisher)

    # Start the subscription in a separate thread
    event_bus.start_subscription_in_thread(
        queue="cleaning_room_booked_queue",
        callback=booking_created_subscriber.handle,
        exchange_type="fanout",
    )
