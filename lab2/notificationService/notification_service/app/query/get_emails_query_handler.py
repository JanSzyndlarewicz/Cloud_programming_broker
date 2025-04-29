from typing import Type

from notification_service.infrastructure.persistence.models.orm_email_log import EmailLog
from notification_service.infrastructure.persistence.repositories.email_log_repository import EmailLogRepository


class GetEmailsQueryHandler:
    def __init__(self, sent_email_repository: EmailLogRepository):
        self.sent_email_repository = sent_email_repository

    def handle(self) -> list[Type[EmailLog]]:
        return self.sent_email_repository.list_all()
