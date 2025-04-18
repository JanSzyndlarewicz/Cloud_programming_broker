from domain.events.booking_created import BookingCreatedEvent
from infrastructure.event_bus.rabbitmq_event_bus import RabbitMQEventBus


class BookingCreatedEventPublisher:
    def __init__(self, event_bus: RabbitMQEventBus):
        self.event_bus = event_bus

    def publish(self, event: BookingCreatedEvent):
        self.event_bus.publish(event, "booking_created")