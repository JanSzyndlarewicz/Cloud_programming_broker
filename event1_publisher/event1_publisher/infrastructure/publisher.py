import pika
import time

from ..application.event1_service import generate_event1
from ..config.logger import logger
from ..config.settings import RABBITMQ_USER, RABBITMQ_PASSWORD, RABBITMQ_HOST, \
    EVENT1_QUEUE, PUBLISH_INTERVAL


class Publisher:
    def __init__(self):
        credentials = pika.PlainCredentials(
            RABBITMQ_USER,
            RABBITMQ_PASSWORD,
        )
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=EVENT1_QUEUE)

    def publish(self):
        while True:
            event = generate_event1()
            message = event.to_json()
            self.channel.basic_publish(exchange='', routing_key=EVENT1_QUEUE, body=message)
            logger.info(f"Published Event1: {message}")
            time.sleep(PUBLISH_INTERVAL)

    def close(self):
        self.connection.close()
