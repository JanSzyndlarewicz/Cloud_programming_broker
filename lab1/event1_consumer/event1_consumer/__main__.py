from .domain.type1_event import Type1Event
from .infrastructure.consumer import Consumer

if __name__ == "__main__":
    consumer = Consumer(Type1Event.__name__)
    try:
        consumer.consume()
    except KeyboardInterrupt:
        consumer.close()