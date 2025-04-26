from pydantic import BaseModel


class InvoiceCreatedEvent(BaseModel):
    invoice_id: int
    order_id: int
    total_amount: float
    status: str  # Status of the invoice (e.g., "pending", "paid")
    issued_date: str  # Issued date as a string (e.g., "YYYY-MM-DD")
    due_date: str  # Due date as a string (e.g., "YYYY-MM-DD")

    # User-related information
    booking_id: int
    guest_name: str
    guest_email: str
    check_in: str  # Check-in date as a string (e.g., "YYYY-MM-DD")
    check_out: str  # Check-out date as a string (e.g., "YYYY-MM-DD")