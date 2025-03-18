from .domain.type1_event import Type1Event
from .infrastructure.publisher import Publisher

if __name__ == "__main__":
    publisher = Publisher(Type1Event.__name__)
    try:
        publisher.publish()
    except KeyboardInterrupt:
        publisher.close()
