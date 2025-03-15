import uuid
import time
from ..domain.event1 import Event1

def generate_event1() -> Event1:
    return Event1(event_id=str(uuid.uuid4()), timestamp=time.time())
