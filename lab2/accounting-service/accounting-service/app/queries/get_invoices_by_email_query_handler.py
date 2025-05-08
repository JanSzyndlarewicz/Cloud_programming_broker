from typing import Type

from infrastructure.persistence.models.orm_invoice import Invoice
from infrastructure.persistence.repositories.invoice_repository import InvoiceRepository


class GetInvoicesByEmailQueryHandler:
    def __init__(self, invoice_repository: InvoiceRepository):
        self.invoice_repository = invoice_repository

    def handle(self, email: str) -> list[Type[Invoice]]:
        return self.invoice_repository.get_invoices_by_email(email)
