import time
import random
from ..config.logger import logger
from ..domain.event3 import Event3

def process_event3(message: str):
    event = Event3.from_json(message)
    time.sleep(random.uniform(2, 5))
    logger.info(f"Processed Event3: {event}")