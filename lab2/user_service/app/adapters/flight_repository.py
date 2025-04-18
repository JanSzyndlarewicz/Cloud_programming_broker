from sqlalchemy.orm import Session

from app.domain.flight_preferences import FlightPreferences
from app.domain.schemas import FlightPreferencesCreate


class FlightPreferencesRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, preference_data: FlightPreferencesCreate) -> FlightPreferences:
        preference = FlightPreferences(**preference_data.model_dump())
        self.db_session.add(preference)
        self.db_session.commit()
        self.db_session.refresh(preference)
        return preference
