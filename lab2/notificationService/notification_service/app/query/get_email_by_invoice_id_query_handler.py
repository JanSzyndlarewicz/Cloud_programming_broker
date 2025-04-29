from notification_service.infrastructure.persistence.models.orm_email_log import EmailLog
from notification_service.infrastructure.persistence.repositories.email_log_repository import EmailLogRepository


class GetEmailByInvoiceIdQueryHandler:
    def __init__(self, sent_email_repository: EmailLogRepository):
        self.sent_email_repository = sent_email_repository

    def handle(self, invoice_id: int) -> EmailLog | None:
        return self.sent_email_repository.get_sent_email_by_invoice_id(invoice_id)
