import uuid
import time

from ..domain.event2 import Event2


def generate_event2() -> Event2:
    return Event2(event_id=str(uuid.uuid4()), timestamp=time.time())
