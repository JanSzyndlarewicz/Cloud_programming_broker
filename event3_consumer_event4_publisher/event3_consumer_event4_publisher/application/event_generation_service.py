import time
import random

from ..domain.type4_event import Type4Event
from .event_processing_service import generate_event4
from ..config.logger import logger
from ..domain.type3_event import Type3Event
from ..infrastructure.producer import Producer


def process_event3(message: str):
    event = Type3Event.from_json(message)
    time.sleep(random.uniform(2, 5))
    logger.info(f"Processed Type3Event: {event}")
    event = generate_event4()
    Producer(Type4Event.__name__).publish_event4(event)