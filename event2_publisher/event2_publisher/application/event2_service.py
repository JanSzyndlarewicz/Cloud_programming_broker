import uuid
import time

from ..domain.type2_event import Type2Event


def generate_event2() -> Type2Event:
    return Type2Event(event_id=str(uuid.uuid4()), timestamp=time.time())
