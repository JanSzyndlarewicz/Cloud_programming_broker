import logging
from datetime import datetime, timedelta
from typing import Optional

from notification_service.app.commands.create_invoice_command import CreateInvoiceCommand
from notification_service.app.events.invoice_created_event_publisher import InvoiceCreatedEventPublisher
from notification_service.domain.events.invoice_created import InvoiceCreatedEvent
from notification_service.infrastructure.database.models import Invoice
from notification_service.infrastructure.database.repositories import InvoiceRepository

logger = logging.getLogger(__name__)


class CreateInvoiceCommandHandler:
    def __init__(
        self,
        invoice_repository: InvoiceRepository,
        event_publisher: InvoiceCreatedEventPublisher,
    ):
        self.invoice_repository = invoice_repository
        self.event_publisher = event_publisher

    def handle(self, command: CreateInvoiceCommand) -> Optional[int]:
        try:
            # Convert and validate check-in and check-out dates
            check_in_date = datetime.strptime(command.check_in, "%Y-%m-%d").date()
            check_out_date = datetime.strptime(command.check_out, "%Y-%m-%d").date()
            due_date = check_out_date + timedelta(days=7)

            # Create invoice
            invoice = Invoice(
                order_id=command.booking_id,
                total_amount=command.total_cost,
                booking_id=command.booking_id,
                guest_name=command.guest_name,
                guest_email=command.guest_email,
                check_in=check_in_date,
                check_out=check_out_date,
                due_date=due_date,
            )

            # Save invoice
            self.invoice_repository.session.add(invoice)
            self.invoice_repository.session.commit()
            self.invoice_repository.session.refresh(invoice)

            # Publish event
            event = InvoiceCreatedEvent(
                invoice_id=invoice.id,
                order_id=invoice.order_id,
                total_amount=invoice.total_amount,
                status=invoice.status,
                issued_date=invoice.issued_date.isoformat(),
                due_date=invoice.due_date.isoformat(),
                booking_id=invoice.booking_id,
                guest_name=invoice.guest_name,
                guest_email=invoice.guest_email,
                check_in=invoice.check_in.isoformat(),
                check_out=invoice.check_out.isoformat(),
            )
            self.event_publisher.publish(event)

            return invoice.id

        except Exception as e:
            logger.info(f"Invoice creation failed: {str(e)}")
            self.invoice_repository.session.rollback()
            raise