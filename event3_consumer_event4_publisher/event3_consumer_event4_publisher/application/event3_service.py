import time
import random

from .event4_service import generate_event4
from ..config.logger import logger
from ..domain.type3_event import Type3Event
from ..infrastructure.producer import Producer


def process_event3(message: str):
    event = Type3Event.from_json(message)
    time.sleep(random.uniform(2, 5))
    logger.info(f"Processed Type3Event: {event}")
    Producer().publish_event4(generate_event4())