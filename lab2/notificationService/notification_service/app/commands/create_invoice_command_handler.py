import logging
from typing import Optional

from app.commands.create_invoice_command import SendEmailCommand
from app.events.email_sent_event_publisher import EmailSentEventPublisher
from app.services.email_service import EmailService
from domain.events.email_sent import EmailSentEvent
from infrastructure.persistence.models.orm_email_log import EmailLog
from infrastructure.persistence.repositories.email_log_repository import EmailLogRepository

logger = logging.getLogger(__name__)


class SendEmailCommandHandler:
    def __init__(
        self,
        email_service: EmailService,
        email_log_repository: EmailLogRepository,
        event_publisher: EmailSentEventPublisher,
    ):
        self.email_service = email_service
        self.email_log_repository = email_log_repository
        self.event_publisher = event_publisher

    def handle(self, command: SendEmailCommand) -> Optional[bool]:
        try:
            # Send email
            self.email_service.send_email(
                recipient=command.recipient_email,
                subject=command.subject,
                body=command.body,
            )
            logger.info(f"Email sent successfully to {command.recipient_email}")

            # Save email log in the persistence
            email_log = EmailLog(
                invoice_id=command.invoice_id,
                recipient_email=command.recipient_email,
                subject=command.subject,
                body=command.body,
                status="sent",
            )
            self.email_log_repository.session.add(email_log)
            self.email_log_repository.session.commit()
            self.email_log_repository.session.refresh(email_log)

            # Publish email sent event
            event = EmailSentEvent(
                email_log_id=email_log.id,
                invoice_id=email_log.invoice_id,
                recipient_email=email_log.recipient_email,
                subject=email_log.subject,
                status=email_log.status,
            )
            self.event_publisher.publish(event)

            return True

        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            self.email_log_repository.session.rollback()
            raise
