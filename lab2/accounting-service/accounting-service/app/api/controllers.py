from app.commands.create_invoice_command import CreateInvoiceCommand
from app.commands.create_invoice_command_handler import CreateInvoiceCommandHandler
from app.queries.get_invoice_query_handler import GetInvoiceQueryHandler
from app.queries.get_invoices_by_email_query_handler import GetInvoicesByEmailQueryHandler
from app.queries.get_invoices_query_handler import GetInvoicesQueryHandler
from fastapi import HTTPException


class InvoiceController:
    def __init__(
        self,
        create_invoice_command_handler: CreateInvoiceCommandHandler,
        get_invoices_query_handler: GetInvoicesQueryHandler,
        get_invoice_query_handler: GetInvoiceQueryHandler,
        get_invoices_by_email_query_handler: GetInvoicesByEmailQueryHandler,
    ):
        self.create_invoice_command_handler = create_invoice_command_handler
        self.get_invoices_query_handler = get_invoices_query_handler
        self.get_invoice_query_handler = get_invoice_query_handler
        self.get_invoices_by_email_query_handler = get_invoices_by_email_query_handler

    async def create_invoice(self, command: CreateInvoiceCommand) -> dict:
        try:
            invoice_id = self.create_invoice_command_handler.handle(command)
            return {"invoice_id": invoice_id, "status": "created"}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def get_invoices(self):
        try:
            return self.get_invoices_query_handler.handle()
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def get_invoice_by_id(self, invoice_id: int):
        try:
            return self.get_invoice_query_handler.handle(invoice_id)
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))

    async def search_invoices_by_email(self, email: str):
        try:
            return self.get_invoices_by_email_query_handler.handle(email)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
