import logging

import pika
import json


class MessageBroker:
    def __init__(self, broker_url: str = 'localhost'):
        self.logger = logging.getLogger(__name__)
        self.broker_url = broker_url
        self.connection = None
        self.channel = None
        self._connect()

    def _connect(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.broker_url))
        self.channel = self.connection.channel()

        # Deklarujemy kolejki, jeśli nie istnieją
        self.channel.queue_declare(queue='user_created', durable=True)
        self.channel.queue_declare(queue='flight_preference_created', durable=True)

    def publish(self, routing_key: str, message: dict):
        self.logger.info(f"Publishing message: {message}")
        if self.channel:
            message_body = json.dumps(message)
            self.channel.basic_publish(
                exchange='',
                routing_key=routing_key,
                body=message_body,
                properties=pika.BasicProperties(
                    delivery_mode=2  # Ustawiamy wiadomość jako trwałą
                )
            )
            self.logger.info(f"Message published to {routing_key} queue.")

    def close(self):
        if self.connection:
            self.connection.close()
