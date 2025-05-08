from dataclasses import dataclass


@dataclass
class CreateDiningCommand:
    guest_name: str
    guest_email: str
    reservation_start_date: str  # Reservation date as a string (e.g., "YYYY-MM-DD")
    reservation_end_date: str  # Reservation date as a string (e.g., "YYYY-MM-DD")
    number_of_guests: int  # Number of guests for the dining reservation
