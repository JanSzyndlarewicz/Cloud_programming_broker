from pydantic import BaseModel
from datetime import date
from typing import Optional

class FlightPreferencesCreate(BaseModel):
    destination: str
    departure_date: date
    return_date: date
    max_price: float
    flight_class: str
    airlines: Optional[str] = None

    class Config:
        orm_mode = True


class UserCreateDTO(BaseModel):
    email: str
    first_name: str
    last_name: str

    class Config:
        orm_mode = True
