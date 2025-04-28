from sqlalchemy.orm import Session

from notification_service.app.events.email_sent_event_publisher import EmailSentEventPublisher
from notification_service.app.events.invoice_created_event_subscriber import InvoiceCreatedEventSubscriber
from notification_service.app.services.email_service import EmailService
from notification_service.infrastructure.config import Config
from notification_service.infrastructure.database.repositories import EmailLogRepository
from notification_service.infrastructure.event_bus.rabbitmq_event_bus import RabbitMQEventBus


def setup_event_subscribers(db: Session, event_bus: RabbitMQEventBus):
    email_log_repository = EmailLogRepository(db)
    email_sent_event_publisher = EmailSentEventPublisher(event_bus)
    email_service = EmailService(
        Config.SMTP_SERVER,
        Config.SMTP_PORT,
        Config.SMTP_USERNAME,
        Config.SMTP_PASSWORD,
    )

    invoice_created_subscriber = InvoiceCreatedEventSubscriber(email_log_repository, email_service,
                                                               email_sent_event_publisher)

    # Subscribe to the "invoice_created" event type
    event_bus.subscribe(
        queue="email_sent_queue", callback=invoice_created_subscriber.handle, exchange_type="direct", routing_key="invoice_created"
    )
