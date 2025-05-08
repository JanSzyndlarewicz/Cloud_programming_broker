from pydantic import BaseModel


class BookingCreatedEvent(BaseModel):
    booking_id: int
    guest_name: str
    guest_email: str
    check_in: str  # Check-in date as a string (e.g., "YYYY-MM-DD")
    check_out: str  # Check-out date as a string (e.g., "YYYY-MM-DD")
    total_cost: float
    number_of_guests: int
    room_number: str
    room_id: int
    meal_reserved: bool  # Indicates if a meal is reserved
