import logging

from infrastructure.config.settings import Config
from infrastructure.messaging.abstract import EventBus

logger = logging.getLogger(__name__)


import json
import logging
from typing import Any

import pika

logger = logging.getLogger(__name__)


class RabbitMQEventBus(EventBus):
    def __init__(self):
        self.broadcast_exchange = "broadcast_events"
        self.direct_exchange = "service_events"

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=Config.RABBITMQ_HOST,
                port=Config.RABBITMQ_PORT,
                credentials=pika.PlainCredentials(Config.RABBITMQ_USER, Config.RABBITMQ_PASSWORD),
                virtual_host=Config.RABBITMQ_VHOST,
            )
        )
        self.channel = self.connection.channel()

        # Fanout exchange - broadcast
        self.channel.exchange_declare(exchange=self.broadcast_exchange, exchange_type="fanout", durable=True)

        # Direct exchange - point-to-point
        self.channel.exchange_declare(exchange=self.direct_exchange, exchange_type="direct", durable=True)

    def publish(self, event: Any, exchange_type: str = "direct", routing_key: str = ""):
        logger.info("Publishing event: %s", event.__dict__)
        exchange = self.direct_exchange if exchange_type == "direct" else self.broadcast_exchange

        self.channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=json.dumps(event.__dict__),
        )

    def subscribe(self, queue: str, callback: callable, exchange_type: str = "direct", routing_key: str = ""):
        exchange = self.direct_exchange if exchange_type == "direct" else self.broadcast_exchange

        self.channel.queue_declare(queue=queue, durable=True)
        self.channel.queue_bind(exchange=exchange, queue=queue, routing_key=routing_key)

        def wrapped_callback(ch, method, properties, body):
            event_data = json.loads(body)
            callback(event_data)

        self.channel.basic_consume(queue=queue, on_message_callback=wrapped_callback, auto_ack=True)
        self.channel.start_consuming()

    def close(self):
        self.channel.close()
        self.connection.close()

    def __del__(self):
        logger.info("Closing RabbitMQ connection in destructor.")
        self.close()
