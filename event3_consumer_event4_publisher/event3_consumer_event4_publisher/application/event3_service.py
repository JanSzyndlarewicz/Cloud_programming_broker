import time
import random
from ..config.logger import logger
from ..domain.type3_event import Type3Event

def process_event3(message: str):
    event = Type3Event.from_json(message)
    time.sleep(random.uniform(2, 5))
    logger.info(f"Processed Type3Event: {event}")