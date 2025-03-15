import time
import random
from ..config.logger import logger
from ..domain.event2 import Event2

def process_event2(message: str):
    event = Event2.from_json(message)
    time.sleep(random.uniform(2, 5))
    logger.info(f"Processed Event2: {event}")