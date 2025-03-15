import time
import random
from ..config.logger import logger
from ..domain.type1_event import Type1Event

def process_event1(message: str):
    event = Type1Event.from_json(message)
    time.sleep(random.uniform(2, 4))
    logger.info(f"Processed Type1Event: {event}")