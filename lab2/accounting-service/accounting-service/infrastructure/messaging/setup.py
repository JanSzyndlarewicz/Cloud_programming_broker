from app.events.booking_created_event_subscriber import BookingCreatedEventSubscriber
from app.events.invoice_created_event_publisher import InvoiceCreatedEventPublisher
from infrastructure.messaging.event_bus import RabbitMQEventBus
from infrastructure.persistence.repositories.invoice_repository import InvoiceRepository
from sqlalchemy.orm import Session


def create_event_subscriber(db: Session, event_bus: RabbitMQEventBus):
    invoice_repository = InvoiceRepository(db)
    event_publisher = InvoiceCreatedEventPublisher(event_bus)
    return BookingCreatedEventSubscriber(invoice_repository, event_publisher)


def setup_event_subscribers(db: Session, event_bus: RabbitMQEventBus, declare_queue: bool = False):
    booking_created_subscriber = create_event_subscriber(db, event_bus)

    result = event_bus.channel.queue_declare(queue="", exclusive=True)
    queue_name = result.method.queue

    event_bus.start_subscription_in_thread(
        queue=queue_name,
        callback=booking_created_subscriber.handle,
        exchange_type="fanout",
        declare_queue=declare_queue,
    )
