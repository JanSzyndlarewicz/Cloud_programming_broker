from cleaning_service.domain.events.cleaning_created import CleaningCreatedEvent
from cleaning_service.infrastructure.event_bus.rabbitmq_event_bus import RabbitMQEventBus


class CleaningCreatedEventPublisher:
    def __init__(self, event_bus: RabbitMQEventBus):
        self.event_bus = event_bus

    def publish(self, event: CleaningCreatedEvent):
        self.event_bus.publish(event, exchange_type="direct", routing_key="cleaning_created")

