from ..config.logger import logger
from ..config.settings import EVENT4
from ..domain.type4_event import Type4Event
from .rabbitmq_connection import RabbitMQConnectionManager

class Producer:
    def __init__(self,  event_type: str):
        self.event_type = event_type
        self.connection = RabbitMQConnectionManager.get_connection()
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.event_type)

    def publish_event4(self, event: Type4Event):
        self.channel.basic_publish(exchange='', routing_key=self.event_type, body=event.to_json())
        logger.info(f"Published Type4Event: {event}")
