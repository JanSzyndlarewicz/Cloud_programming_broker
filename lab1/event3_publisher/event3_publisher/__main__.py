from .infrastructure.publisher import Publisher

if __name__ == "__main__":
    publisher = Publisher()
    try:
        publisher.publish()
    except KeyboardInterrupt:
        publisher.close()
