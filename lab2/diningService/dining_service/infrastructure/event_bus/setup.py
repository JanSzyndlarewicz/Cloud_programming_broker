from sqlalchemy.orm import Session

from dining_service.app.events.booking_created_event_subscriber import BookingCreatedEventSubscriber
from dining_service.app.events.dining_created_event_publisher import DiningCreatedEventPublisher
from dining_service.infrastructure.database.repositories import DiningReservationRepository
from dining_service.infrastructure.event_bus.rabbitmq_event_bus import RabbitMQEventBus


def setup_event_subscribers(db: Session, event_bus: RabbitMQEventBus):
    dining_repository = DiningReservationRepository(db)
    event_publisher = DiningCreatedEventPublisher(event_bus)

    booking_created_subscriber = BookingCreatedEventSubscriber(
        dining_repository, event_publisher
    )

    # Subscribe to the "booking_created" event type
    event_bus.subscribe(
        queue=f"dining_room_booked_queue",
        callback=booking_created_subscriber.handle,
        exchange_type="fanout"
    )