import logging
from datetime import datetime

from notification_service.app.events.email_sent_event_publisher import EmailSentEventPublisher
from notification_service.app.services.email_service import EmailService
from notification_service.domain.events.email_sent import EmailSentEvent
from notification_service.domain.events.invoice_created import InvoiceCreatedEvent
from notification_service.infrastructure.database.models import EmailLog
from notification_service.infrastructure.database.repositories import EmailLogRepository

logger = logging.getLogger(__name__)


class InvoiceCreatedEventSubscriber:
    def __init__(
        self,
        email_log_repository: EmailLogRepository,
        email_service: EmailService,
        event_publisher: EmailSentEventPublisher,
    ):
        self.email_log_repository = email_log_repository
        self.email_service = email_service
        self.event_publisher = event_publisher

    def handle(self, event: dict):
        logger.info(f"Handling InvoiceCreatedEvent: {event}")
        try:
            # Convert dictionary to InvoiceCreatedEvent
            logger.info(f"Converting event to InvoiceCreatedEvent: {event}")
            event_obj = InvoiceCreatedEvent(**event)
            logger.info(f"Converted event: {event_obj.model_dump()}")

            # Send email
            subject = f"Invoice #{event_obj.invoice_id}"
            body = f"Dear {event_obj.guest_name},\n\nYour invoice is attached.\n\nTotal: {event_obj.total_amount}"
            self.email_service.send_email(event_obj.guest_email, subject, body)

            # Save sent email details
            sent_email = EmailLog(
                invoice_id=event_obj.invoice_id,
                recipient_email=event_obj.guest_email,
                subject=subject,
                body=body,
                status="sent",
            )
            self.email_log_repository.session.add(sent_email)
            self.email_log_repository.session.commit()

            # Publish EmailSentEvent
            email_sent_event = EmailSentEvent(
                invoice_id=event_obj.invoice_id,
                email=event_obj.guest_email,
                status="sent",
                sent_date=datetime.now().isoformat(),
            )
            self.event_publisher.publish(email_sent_event)

        except Exception as e:
            logger.error(f"Failed to handle InvoiceCreatedEvent: {str(e)}")
            self.email_log_repository.session.rollback()
            raise
