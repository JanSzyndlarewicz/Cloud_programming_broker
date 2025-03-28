import pika
from ..config.settings import RABBITMQ_HOST, RABBITMQ_USER, RABBITMQ_PASSWORD

class RabbitMQConnectionManager:
    _connection = None

    @classmethod
    def get_connection(cls):
        if cls._connection is None or cls._connection.is_closed:
            credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
            cls._connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials))
        return cls._connection
