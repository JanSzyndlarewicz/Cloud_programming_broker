from pydantic import BaseModel, EmailStr


class Room(BaseModel):
    room_id: int
    nights: int


class CreateBookingRequest(BaseModel):
    guest_name: str
    guest_email: EmailStr
    room: Room
    check_in: str
    check_out: str
    number_of_guests: int
    meal_reserved: bool = False
