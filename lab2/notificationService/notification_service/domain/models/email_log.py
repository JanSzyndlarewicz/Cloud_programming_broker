from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, func

Base = declarative_base()

class EmailLog(Base):
    __tablename__ = "sent_emails"

    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, nullable=False)  # Reference to the invoice
    recipient_email = Column(String, nullable=False)  # Email of the recipient
    subject = Column(String, nullable=False)  # Subject of the email
    body = Column(String, nullable=False)  # Body of the email
    sent_date = Column(DateTime, nullable=False, server_default=func.now())  # Date and time the email was sent
    status = Column(String(50), nullable=False, default="sent")  # Status of the email (e.g., sent, failed)