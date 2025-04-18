import logging

from sqlalchemy.orm import Session

from app.adapters.flight_repository import FlightPreferencesRepository
from app.domain.flight_preferences import FlightPreferences
from app.domain.schemas import FlightPreferencesCreate
from app.domain.user import User


class FlightPreferencesUseCase:
    def __init__(self, flight_preferences_repository: FlightPreferencesRepository):
        self.logger = logging.getLogger(__name__)
        self.flight_preferences_repository = flight_preferences_repository

    def create_flight_preferences(self, db: Session, user_id: int, flight_preferences: FlightPreferencesCreate):
        self.logger.debug(f"Creating flight preferences for user {user_id}")
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")

        new_preference = FlightPreferences(
            user_id=user.id,
            destination=flight_preferences.destination,
            departure_date=flight_preferences.departure_date,
            return_date=flight_preferences.return_date,
            max_price=flight_preferences.max_price,
            flight_class=flight_preferences.flight_class,
            airlines=flight_preferences.airlines
        )
        db.add(new_preference)
        db.commit()
        db.refresh(new_preference)

        self.logger.debug(f"Flight preferences created for user {user_id}")

        self._publish_flight_preference_created(new_preference)

        return new_preference

    def _publish_flight_preference_created(self, preference):
        pass

