from datetime import datetime
from typing import List, Type

from sqlalchemy.orm import Session

from notification_service.infrastructure.database.models import Invoice


class InvoiceRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_invoice(self, order_id: int, total_amount: float, due_date: str) -> Invoice:
        due_date_obj = datetime.strptime(due_date, "%Y-%m-%d").date()
        invoice = Invoice(order_id=order_id, total_amount=total_amount, due_date=due_date_obj)
        self.session.add(invoice)
        self.session.commit()
        self.session.refresh(invoice)
        return invoice

    def get_invoice(self, invoice_id: int) -> Invoice | None:
        return self.session.query(Invoice).filter(Invoice.id == invoice_id).first()

    def list_all(self) -> list[Type[Invoice]]:
        return self.session.query(Invoice).all()

    def get_invoices_by_email(self, email: str) -> list[Type[Invoice]]:
        return self.session.query(Invoice).filter(Invoice.guest_email == email).all()