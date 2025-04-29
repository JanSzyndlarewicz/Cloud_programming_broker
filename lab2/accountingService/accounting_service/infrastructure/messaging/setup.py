from accounting_service.app.events.booking_created_event_subscriber import BookingCreatedEventSubscriber
from accounting_service.app.events.invoice_created_event_publisher import InvoiceCreatedEventPublisher
from accounting_service.infrastructure.messaging.event_bus import RabbitMQEventBus
from sqlalchemy.orm import Session

from accounting_service.infrastructure.persistence.repositories.invoice_repository import InvoiceRepository


def create_event_subscriber(db: Session, event_bus: RabbitMQEventBus):
    invoice_repository = InvoiceRepository(db)
    event_publisher = InvoiceCreatedEventPublisher(event_bus)
    return BookingCreatedEventSubscriber(invoice_repository, event_publisher)


def setup_event_subscribers(db: Session, event_bus: RabbitMQEventBus, declare_queue: bool = False):
    booking_created_subscriber = create_event_subscriber(db, event_bus)

    result = event_bus.channel.queue_declare(queue="", exclusive=True)
    queue_name = result.method.queue

    # Subskrybujemy tylko fanout broadcast z przekazaniem flagi declare_queue
    event_bus.subscribe(
        queue=queue_name,
        callback=booking_created_subscriber.handle,
        exchange_type="fanout",
        declare_queue=declare_queue,
    )
