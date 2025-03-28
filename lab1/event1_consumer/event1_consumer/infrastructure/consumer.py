import pika

from ..application.event_service import process_event
from ..config.logger import logger
from ..config.settings import RABBITMQ_HOST, RABBITMQ_USER, RABBITMQ_PASSWORD


class Consumer:
    def __init__(self, event_type: str):
        self.event_type = event_type
        credentials = pika.PlainCredentials(
            RABBITMQ_USER,
            RABBITMQ_PASSWORD,
        )
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.event_type)

    def consume(self):
        def callback(ch, method, properties, body):
            process_event(body.decode())

        self.channel.basic_consume(queue=self.event_type, on_message_callback=callback, auto_ack=True)
        logger.info('Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

    def close(self):
        self.connection.close()