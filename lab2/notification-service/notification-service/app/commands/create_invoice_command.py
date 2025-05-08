from dataclasses import dataclass


@dataclass
class SendEmailCommand:
    invoice_id: int
    recipient_email: str
    subject: str
    body: str
