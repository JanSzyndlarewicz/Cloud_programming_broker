from datetime import datetime
from typing import List, Type

from sqlalchemy.orm import Session

from notification_service.infrastructure.persistence.models.orm_email_log import EmailLog


class EmailLogRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_sent_email(
        self, invoice_id: int, recipient_email: str, subject: str, body: str, status: str = "sent"
    ) -> EmailLog:
        sent_email = EmailLog(
            invoice_id=invoice_id,
            recipient_email=recipient_email,
            subject=subject,
            body=body,
            status=status,
            sent_date=datetime.now(),
        )
        self.session.add(sent_email)
        self.session.commit()
        self.session.refresh(sent_email)
        return sent_email

    def get_sent_email(self, email_id: int) -> EmailLog | None:
        return self.session.query(EmailLog).filter(EmailLog.id == email_id).first()

    def get_sent_email_by_invoice_id(self, invoice_id: int) -> EmailLog | None:
        return self.session.query(EmailLog).filter(EmailLog.invoice_id == invoice_id).first()

    def get_sent_emails_by_recipient_email(self, recipient_email: str) -> List[EmailLog]:
        return self.session.query(EmailLog).filter(EmailLog.recipient_email == recipient_email).all()

    def list_all(self) -> list[Type[EmailLog]]:
        return self.session.query(EmailLog).all()
