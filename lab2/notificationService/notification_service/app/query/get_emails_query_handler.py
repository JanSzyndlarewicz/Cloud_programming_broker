from typing import List, Type

from notification_service.infrastructure.database.models import EmailLog
from notification_service.infrastructure.database.repositories import EmailLogRepository


class GetEmailsQueryHandler:
    def __init__(self, sent_email_repository: EmailLogRepository):
        self.sent_email_repository = sent_email_repository

    def handle(self) -> list[Type[EmailLog]]:
        return self.sent_email_repository.list_all()