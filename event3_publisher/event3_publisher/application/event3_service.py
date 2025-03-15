import uuid
import time
from ..domain.event3 import Event3

def generate_event3() -> Event3:
    return Event3(event_id=str(uuid.uuid4()), timestamp=time.time())
