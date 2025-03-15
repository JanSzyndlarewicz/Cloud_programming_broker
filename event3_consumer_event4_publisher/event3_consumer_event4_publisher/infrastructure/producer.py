import pika

from ..config.logger import logger
from ..config.settings import RABBITMQ_HOST, EVENT4, RABBITMQ_USER, RABBITMQ_PASSWORD
from ..domain.type4_event import Type4Event


class Producer:
    def __init__(self):
        credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=EVENT4)

    def publish_event4(self, event: Type4Event):
        self.channel.basic_publish(exchange='', routing_key=EVENT4, body=event.to_json())
        logger.info(f"Published Type4Event: {event}")

    def close(self):
        self.connection.close()