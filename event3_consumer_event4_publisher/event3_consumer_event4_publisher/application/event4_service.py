import uuid
import time

from ..domain.type4_event import Type4Event


def generate_event4() -> Type4Event:
    return Type4Event(event_id=str(uuid.uuid4()), timestamp=time.time())
