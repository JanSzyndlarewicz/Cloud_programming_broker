from .infrastructure.consumer import Consumer
from .infrastructure.producer import Producer
from .domain.event4 import Event4
import time
import random

if __name__ == "__main__":
    consumer = Consumer()
    producer = Producer()
    try:
        while True:
            consumer.consume()
            # Simulate producing an event4 after consuming an event3
            event4 = Event4(event_id="event4_id", timestamp=time.time())
            producer.publish_event4(event4)
            time.sleep(random.uniform(2, 5))  # Delay between producing events
    except KeyboardInterrupt:
        consumer.close()
        producer.close()