import time
import random
from ..config.logger import logger
from ..domain.event4 import Event4

def process_event4(message: str):
    event = Event4.from_json(message)
    time.sleep(random.uniform(2, 5))
    logger.info(f"Processed Event4: {event}")