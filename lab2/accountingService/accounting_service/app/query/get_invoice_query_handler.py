from accounting_service.infrastructure.database.models import Invoice
from accounting_service.infrastructure.database.repositories import InvoiceRepository


class GetInvoiceQueryHandler:
    def __init__(self, invoice_repository: InvoiceRepository):
        self.invoice_repository = invoice_repository

    def handle(self, invoice_id: int) -> Invoice | None:
        return self.invoice_repository.get_invoice(invoice_id)