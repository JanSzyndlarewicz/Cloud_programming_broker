import logging
from datetime import datetime, timedelta

from app.events.invoice_created_event_publisher import InvoiceCreatedEventPublisher
from domain.events.booking_created import BookingCreatedEvent
from domain.events.invoice_created import InvoiceCreatedEvent
from infrastructure.persistence.models.orm_invoice import Invoice
from infrastructure.persistence.repositories.invoice_repository import InvoiceRepository

logger = logging.getLogger(__name__)


class BookingCreatedEventSubscriber:
    def __init__(
        self,
        invoice_repository: InvoiceRepository,
        event_publisher: InvoiceCreatedEventPublisher,
    ):
        self.invoice_repository = invoice_repository
        self.event_publisher = event_publisher

    def handle(self, event: dict):
        logger.info(f"Handling BookingCreatedEvent: {event}")
        try:
            # Convert dictionary to BookingCreatedEvent
            logger.info(f"Converting event to BookingCreatedEvent: {event}")
            event_obj = BookingCreatedEvent(**event)
            logger.info(f"Converted event: {event_obj.model_dump()}")

            # Create an invoice for the booking
            due_date = datetime.strptime(event_obj.check_out, "%Y-%m-%d").date() + timedelta(days=7)
            invoice = Invoice(
                order_id=event_obj.booking_id,
                total_amount=event_obj.total_cost,
                booking_id=event_obj.booking_id,
                guest_name=event_obj.guest_name,
                guest_email=event_obj.guest_email,
                check_in=datetime.strptime(event_obj.check_in, "%Y-%m-%d").date(),
                check_out=datetime.strptime(event_obj.check_out, "%Y-%m-%d").date(),
                due_date=due_date,
            )
            self.invoice_repository.session.add(invoice)
            self.invoice_repository.session.commit()  # Commit to generate the ID

            invoice_event = InvoiceCreatedEvent(
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
            self.event_publisher.publish(invoice_event)

        except Exception as e:
            logger.error(f"Failed to handle BookingCreatedEvent: {str(e)}")
            self.invoice_repository.session.rollback()
            raise
