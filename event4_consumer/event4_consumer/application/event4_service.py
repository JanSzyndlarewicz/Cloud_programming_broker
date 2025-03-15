import time
import random
from ..config.logger import logger
from ..domain.type4_event import Type4Event

def process_event4(message: str):
    event = Type4Event.from_json(message)
    time.sleep(random.uniform(2, 5))
    logger.info(f"Processed Type4Event: {event}")