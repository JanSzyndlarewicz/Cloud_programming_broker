import time
import random
from ..config.logger import logger
from ..domain.event1 import Event1

def process_event1(message: str):
    event = Event1.from_json(message)
    time.sleep(random.uniform(2, 4))
    logger.info(f"Processed Event1: {event}")