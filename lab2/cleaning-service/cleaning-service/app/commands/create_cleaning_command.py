from dataclasses import dataclass


@dataclass
class CreateCleaningCommand:
    room_id: int
    cleaning_date: str
    cleaning_type: str
    assigned_staff: str
