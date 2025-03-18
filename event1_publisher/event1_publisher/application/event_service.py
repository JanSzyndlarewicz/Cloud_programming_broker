import time
import uuid

from ..domain import event_types
from ..domain.type_event import TypeEvent

def generate_event(event_type: str) -> TypeEvent:
    for event in event_types:
        if event.__name__ == event_type:
            return event(event_id=str(uuid.uuid4()), timestamp=time.time())
    raise ValueError(f"Unknown event type: {event_type}")