from typing import Type

from accounting_service.infrastructure.database.models import Invoice
from accounting_service.infrastructure.database.repositories import InvoiceRepository


class GetInvoicesByEmailQueryHandler:
    def __init__(self, invoice_repository: InvoiceRepository):
        self.invoice_repository = invoice_repository

    def handle(self, email: str) -> list[Type[Invoice]]:
        return self.invoice_repository.get_invoices_by_email(email)
