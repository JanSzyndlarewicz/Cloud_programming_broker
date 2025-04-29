from accounting_service.infrastructure.persistence.models.orm_invoice import Invoice
from accounting_service.infrastructure.persistence.repositories.invoice_repository import InvoiceRepository


class GetInvoiceQueryHandler:
    def __init__(self, invoice_repository: InvoiceRepository):
        self.invoice_repository = invoice_repository

    def handle(self, invoice_id: int) -> Invoice | None:
        return self.invoice_repository.get_invoice(invoice_id)
