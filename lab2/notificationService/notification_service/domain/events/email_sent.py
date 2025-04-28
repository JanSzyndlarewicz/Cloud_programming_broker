from pydantic import BaseModel


class EmailSentEvent(BaseModel):
    invoice_id: int
    email: str
    status: str  # e.g., "sent"
    sent_date: str  # e.g., "YYYY-MM-DDTHH:MM:SS"
