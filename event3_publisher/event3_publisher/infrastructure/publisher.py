import random
import time

import pika

from ..application.event_service import generate_event3
from ..config.logger import logger
from ..config.settings import RABBITMQ_HOST, EVENT3, RABBITMQ_USER, RABBITMQ_PASSWORD


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
        self.channel.queue_declare(queue=EVENT3)

    def publish(self):
        while True:
            event = generate_event3()
            message = event.to_json()
            self.channel.basic_publish(exchange='', routing_key=EVENT3, body=message)
            logger.info(f"Published Type3Event: {message}")
            time.sleep(random.uniform(4, 8))

    def close(self):
        self.connection.close()
