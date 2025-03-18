import random
import time

from .infrastructure.consumer import Consumer
from .infrastructure.producer import Producer

if __name__ == "__main__":
    consumer = Consumer()
    producer = Producer()
    try:
        while True:
            consumer.consume()
            time.sleep(random.uniform(2, 5))
    except KeyboardInterrupt:
        consumer.connection.close()
        producer.connection.close()