import uuid
import time
from ..domain.type3_event import Type3Event

def generate_event3() -> Type3Event:
    return Type3Event(event_id=str(uuid.uuid4()), timestamp=time.time())
