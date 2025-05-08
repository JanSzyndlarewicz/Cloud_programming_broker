from app.api.controllers import InvoiceController
from app.queries.get_invoices_query_handler import GetInvoicesQueryHandler
from infrastructure.persistence import get_db
from infrastructure.persistence.repositories.invoice_repository import InvoiceRepository
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()


def get_invoice_controller(db: Session = Depends(get_db)):
    invoice_repository = InvoiceRepository(db)
    return InvoiceController(GetInvoicesQueryHandler(invoice_repository))


@router.get("/invoices")
async def list_invoices(controller: InvoiceController = Depends(get_invoice_controller)):
    return await controller.get_invoices()


@router.get("/invoices/{invoice_id}")
async def get_invoice_by_id(invoice_id: int, controller: InvoiceController = Depends(get_invoice_controller)):
    return await controller.get_invoice_by_id(invoice_id)


@router.get("/invoices/search")
async def search_invoices_by_email(email: str, controller: InvoiceController = Depends(get_invoice_controller)):
    return await controller.search_invoices_by_email(email)
