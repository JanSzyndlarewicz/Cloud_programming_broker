import pika
import time
from ..config.settings import RABBITMQ_HOST, EVENT3_QUEUE, PUBLISH_INTERVAL, RABBITMQ_USER, RABBITMQ_PASSWORD
from ..config.logger import logger
from ..application.event3_service import generate_event3


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
        self.channel.queue_declare(queue=EVENT3_QUEUE)

    def publish(self):
        while True:
            event = generate_event3()
            message = event.to_json()
            self.channel.basic_publish(exchange='', routing_key=EVENT3_QUEUE, body=message)
            logger.info(f"Published Event3: {message}")
            time.sleep(PUBLISH_INTERVAL)

    def close(self):
        self.connection.close()
