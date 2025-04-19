from cleaning_service.app.events.booking_created_event_subscriber import BookingCreatedEventSubscriber
from cleaning_service.infrastructure.config import Config
from cleaning_service.infrastructure.database.repositories import CleaningRepository, RoomRepository
from cleaning_service.app.events.cleaning_created_event_publisher import CleaningCreatedEventPublisher
from cleaning_service.infrastructure.event_bus.rabbitmq_event_bus import RabbitMQEventBus
from sqlalchemy.orm import Session

def setup_event_subscribers(db: Session, event_bus: RabbitMQEventBus):
    cleaning_repository = CleaningRepository(db)
    room_repository = RoomRepository(db)
    event_publisher = CleaningCreatedEventPublisher(event_bus)

    booking_created_subscriber = BookingCreatedEventSubscriber(
        cleaning_repository, room_repository, event_publisher
    )

    # Subscribe to the "booking_created" event type
    event_bus.subscribe(
        queue=f"{Config.RABBITMQ_EXCHANGE}_queue",
        callback=booking_created_subscriber.handle,
        routing_key="booking_created"
    )