import pika

from ..config.logger import logger
from ..config.settings import RABBITMQ_HOST, EVENT4_QUEUE, RABBITMQ_USER, RABBITMQ_PASSWORD
from ..application.event4_service import process_event4

class Consumer:
    def __init__(self):
        credentials = pika.PlainCredentials(
            RABBITMQ_USER,
            RABBITMQ_PASSWORD,
        )
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=EVENT4_QUEUE)

    def consume(self):
        def callback(ch, method, properties, body):
            process_event4(body.decode())

        self.channel.basic_consume(queue=EVENT4_QUEUE, on_message_callback=callback, auto_ack=True)
        logger.info('Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

    def close(self):
        self.connection.close()