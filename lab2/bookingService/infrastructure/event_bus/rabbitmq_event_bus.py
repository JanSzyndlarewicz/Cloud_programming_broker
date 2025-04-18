import json
from typing import Any

import pika
from infrastructure.config import Config
from infrastructure.event_bus.abstractions import EventBus


class RabbitMQEventBus(EventBus):
    def __init__(self):
        self.exchange = Config.RABBITMQ_EXCHANGE
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=Config.RABBITMQ_HOST,
                port=Config.RABBITMQ_PORT,
                credentials=pika.PlainCredentials(Config.RABBITMQ_USER, Config.RABBITMQ_PASSWORD),
            )
        )
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self.exchange, exchange_type="fanout", durable=True)

        self.channel.queue_declare(queue=f"{self.exchange}_queue", durable=True)
        self.channel.queue_bind(exchange=self.exchange, queue=f"{self.exchange}_queue")

    def publish(self, event: Any, routing_key: str):
        print("Publishing event:", event.__dict__)
        self.channel.basic_publish(
            exchange=self.exchange,
            body=json.dumps(event.__dict__),
            routing_key=routing_key,
        )

    def subscribe(self, queue: str, callback: callable, routing_key: str = None):
        self.channel.queue_declare(queue=queue)
        if routing_key:
            self.channel.queue_bind(queue=queue, routing_key=routing_key)

        def wrapped_callback(ch, method, properties, body):
            event_data = json.loads(body)
            callback(event_data)

        self.channel.basic_consume(queue=queue, on_message_callback=wrapped_callback, auto_ack=True)

        self.channel.start_consuming()

    def close(self):
        self.connection.close()
