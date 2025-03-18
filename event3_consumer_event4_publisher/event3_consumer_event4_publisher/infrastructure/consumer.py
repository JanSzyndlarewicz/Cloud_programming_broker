from ..config.logger import logger
from ..config.settings import EVENT3
from ..application.event3_service import process_event3
from .rabbitmq_connection import RabbitMQConnectionManager

class Consumer:
    def __init__(self):
        self.connection = RabbitMQConnectionManager.get_connection()
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=EVENT3)

    def consume(self):
        def callback(ch, method, properties, body):
            process_event3(body.decode())

        self.channel.basic_consume(queue=EVENT3, on_message_callback=callback, auto_ack=True)
        logger.info('Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()