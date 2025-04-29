from dining_service.domain.events.dining_created import DiningCreatedEvent
from dining_service.infrastructure.config.settings import Config
from dining_service.infrastructure.messaging.event_bus import RabbitMQEventBus


class DiningCreatedEventPublisher:
    def __init__(self, event_bus: RabbitMQEventBus):
        self.event_bus = event_bus

    def publish(self, event: DiningCreatedEvent):
        self.event_bus.publish(event, exchange_type="direct", routing_key=Config.DINING_CREATED_ROUTING_KEY)
