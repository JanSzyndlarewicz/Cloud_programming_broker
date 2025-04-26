from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, Float, String, Date, func

Base = declarative_base()

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, nullable=False)  # Reference to the order
    total_amount = Column(Float, nullable=False)  # Total amount for the invoice
    status = Column(String(50), nullable=False, default="pending")  # Invoice status (e.g., pending, paid)
    issued_date = Column(Date, nullable=False, server_default=func.now())  # Date of issuance
    due_date = Column(Date, nullable=False)  # Payment due date

    # User-related information
    booking_id = Column(Integer, nullable=False)  # Reference to the booking
    guest_name = Column(String, nullable=False)  # Name of the guest
    guest_email = Column(String, nullable=False)  # Email of the guest
    check_in = Column(Date, nullable=False)  # Check-in date
    check_out = Column(Date, nullable=False)  # Check-out date