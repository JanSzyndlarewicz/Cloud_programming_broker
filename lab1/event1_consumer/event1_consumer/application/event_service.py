import random
import time

from ..domain.type_event import TypeEvent
from ..config.logger import logger


def process_event(message: str):
    event = TypeEvent.from_json(message)
    time.sleep(random.uniform(2, 4))
    logger.info(f"Processed Type1Event: {event}")