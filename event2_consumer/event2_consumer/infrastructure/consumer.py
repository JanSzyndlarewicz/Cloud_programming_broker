import pika

from ..config.logger import logger
from ..config.settings import RABBITMQ_HOST, EVENT2_QUEUE, RABBITMQ_USER, RABBITMQ_PASSWORD
from ..application.event2_service import process_event2

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
        self.channel.queue_declare(queue=EVENT2_QUEUE)

    def consume(self):
        def callback(ch, method, properties, body):
            process_event2(body.decode())

        self.channel.basic_consume(queue=EVENT2_QUEUE, on_message_callback=callback, auto_ack=True)
        logger.info('Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

    def close(self):
        self.connection.close()