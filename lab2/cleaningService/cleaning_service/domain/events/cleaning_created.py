from pydantic import BaseModel


class CleaningCreatedEvent(BaseModel):
    cleaning_id: int
    room_id: int
    room_number: str
    cleaning_date: str  # Cleaning date as a string (e.g., "YYYY-MM-DD")
    cleaning_type: str  # Type of cleaning (e.g., "standard", "deep")
    assigned_staff: str  # Name or ID of the staff assigned to the cleaning
