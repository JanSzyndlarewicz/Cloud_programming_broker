from app.events.email_sent_event_publisher import EmailSentEventPublisher
from app.events.invoice_created_event_subscriber import InvoiceCreatedEventSubscriber
from app.services.email_service import EmailService
from infrastructure.config.settings import Config
from infrastructure.messaging.event_bus import RabbitMQEventBus
from infrastructure.persistence.repositories.email_log_repository import EmailLogRepository
from sqlalchemy.orm import Session


def setup_event_subscribers(db: Session, event_bus: RabbitMQEventBus):
    email_log_repository = EmailLogRepository(db)
    email_sent_event_publisher = EmailSentEventPublisher(event_bus)
    email_service = EmailService(
        Config.SMTP_SERVER,
        Config.SMTP_PORT,
        Config.SMTP_USERNAME,
        Config.SMTP_PASSWORD,
    )

    invoice_created_subscriber = InvoiceCreatedEventSubscriber(
        email_log_repository, email_service, email_sent_event_publisher
    )

    # Subscribe to the "invoice_created" event type
    event_bus.start_subscription_in_thread(
        queue="email_sent_queue",
        callback=invoice_created_subscriber.handle,
        exchange_type="direct",
        routing_key=Config.INVOICE_CREATED_ROUTING_KEY,
    )
