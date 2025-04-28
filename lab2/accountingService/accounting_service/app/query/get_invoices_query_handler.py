from accounting_service.infrastructure.database.repositories import InvoiceRepository


class GetInvoicesQueryHandler:
    def __init__(self, invoice_repository: InvoiceRepository):
        self.invoice_repository = invoice_repository

    def handle(self) -> list:
        return self.invoice_repository.list_all()
