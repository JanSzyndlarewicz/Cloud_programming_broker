import time
import random
from ..config.logger import logger
from ..domain.type2_event import Type2Event

def process_event2(message: str):
    event = Type2Event.from_json(message)
    time.sleep(random.uniform(2, 5))
    logger.info(f"Processed Type2Event: {event}")