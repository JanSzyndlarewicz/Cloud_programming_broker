import uuid
import time
from ..domain.type1_event import Type1Event

def generate_event1() -> Type1Event:
    return Type1Event(event_id=str(uuid.uuid4()), timestamp=time.time())
