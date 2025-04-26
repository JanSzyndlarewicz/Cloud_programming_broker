from notification_service.domain.events.invoice_created import InvoiceCreatedEvent
from notification_service.infrastructure.event_bus.rabbitmq_event_bus import RabbitMQEventBus


class InvoiceCreatedEventPublisher:
    def __init__(self, event_bus: RabbitMQEventBus):
        self.event_bus = event_bus

    def publish(self, event: InvoiceCreatedEvent):
        self.event_bus.publish(event, exchange_type="direct", routing_key="invoice_created")