from app.domain.flight_preferences import FlightPreferences
from app.domain.user import User
from app.infrastructure.message_broker import MessageBroker


class EventPublisher:
    def __init__(self, message_broker: MessageBroker):
        self.message_broker = message_broker

    def publish_user_created_event(self, user: User):
        event_data = {"user_id": user.id, "email": user.email}
        self.message_broker.publish("user_created", event_data)

    def publish_flight_preference_created_event(self, preference: FlightPreferences):
        event_data = {
            "user_id": preference.user_id,
            "destination": preference.destination,
            "departure_date": preference.departure_date
        }
        self.message_broker.publish("flight_preference_created", event_data)
