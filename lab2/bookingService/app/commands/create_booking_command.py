from dataclasses import dataclass


@dataclass
class CreateBookingCommand:
    guest_name: str
    guest_email: str
    room: dict
    check_in: str
    check_out: str