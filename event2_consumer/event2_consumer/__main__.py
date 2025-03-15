from .infrastructure.consumer import Consumer

if __name__ == "__main__":
    consumer = Consumer()
    try:
        consumer.consume()
    except KeyboardInterrupt:
        consumer.close()