from accounting_service.app.events.booking_created_event_subscriber import BookingCreatedEventSubscriber
from accounting_service.app.events.invoice_created_event_publisher import InvoiceCreatedEventPublisher
from accounting_service.infrastructure.database.repositories import InvoiceRepository

from accounting_service.infrastructure.event_bus.rabbitmq_event_bus import RabbitMQEventBus
from sqlalchemy.orm import Session


def setup_event_subscribers(db: Session, event_bus: RabbitMQEventBus):
    invoice_repository = InvoiceRepository(db)
    event_publisher = InvoiceCreatedEventPublisher(event_bus)

    booking_created_subscriber = BookingCreatedEventSubscriber(invoice_repository, event_publisher)

    # Subscribe to the "booking_created" event type
    event_bus.subscribe(
        queue=f"invoice_created_queue", callback=booking_created_subscriber.handle, exchange_type="fanout"
    )
