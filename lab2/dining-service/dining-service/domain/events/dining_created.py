from pydantic import BaseModel


class DiningCreatedEvent(BaseModel):
    dining_id: int
    guest_name: str
    guest_email: str
    reservation_date: str  # Reservation date as a string (e.g., "YYYY-MM-DD")
    number_of_guests: int  # Number of guests for the dining reservation
