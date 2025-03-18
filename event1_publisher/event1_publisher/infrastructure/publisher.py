import time

import pika

from ..application.event_service import generate_event
from ..config.logger import logger
from ..config.settings import RABBITMQ_USER, RABBITMQ_PASSWORD, RABBITMQ_HOST, PUBLISH_INTERVAL


class Publisher:
    def __init__(self, event_type: str):
        self.event_type = event_type
        credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=event_type)

    def publish(self):
        while True:
            event = generate_event(self.event_type)
            message = event.to_json()
            self.channel.basic_publish(exchange='', routing_key=self.event_type, body=message)
            logger.info(f"Published Type1Event: {message}")
            time.sleep(PUBLISH_INTERVAL)

    def close(self):
        self.connection.close()
