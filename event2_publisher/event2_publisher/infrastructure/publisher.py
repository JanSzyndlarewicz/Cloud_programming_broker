import random
import time

import pika

from ..application.event2_service import generate_event2
from ..config.logger import logger
from ..config.settings import RABBITMQ_USER, RABBITMQ_PASSWORD, RABBITMQ_HOST, EVENT2_QUEUE


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
        self.channel.queue_declare(queue=EVENT2_QUEUE)

    def publish(self):
        while True:
            event = generate_event2()
            message = event.to_json()
            self.channel.basic_publish(exchange='', routing_key=EVENT2_QUEUE, body=message)
            logger.info(f"Published Type2Event: {message}")
            time.sleep(random.uniform(4, 8))

    def close(self):
        self.connection.close()
