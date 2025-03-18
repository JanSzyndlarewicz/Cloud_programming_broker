import random
import time

from .infrastructure.consumer import Consumer

if __name__ == "__main__":
    consumer = Consumer()
    try:
        while True:
            consumer.consume()
            time.sleep(random.uniform(2, 5))
    except KeyboardInterrupt:
        consumer.connection.close()
