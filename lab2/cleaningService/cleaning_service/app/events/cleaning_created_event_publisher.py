from domain.events.cleaning_created import CleaningCreatedEvent
from infrastructure.config.settings import Config
from infrastructure.messaging.event_bus import RabbitMQEventBus


class CleaningCreatedEventPublisher:
    def __init__(self, event_bus: RabbitMQEventBus):
        self.event_bus = event_bus

    def publish(self, event: CleaningCreatedEvent):
        self.event_bus.publish(event, exchange_type="direct", routing_key=Config.CLEANING_CREATED_ROUTING_KEY)
