from notification_service.infrastructure.database.models import EmailLog
from notification_service.infrastructure.database.repositories import EmailLogRepository


class GetEmailsByMailRecipientQueryHandler:
    def __init__(self, sent_email_repository: EmailLogRepository):
        self.sent_email_repository = sent_email_repository

    def handle(self, mail_recipient: str) -> list[EmailLog]:
        return self.sent_email_repository.get_sent_emails_by_recipient_email(mail_recipient)