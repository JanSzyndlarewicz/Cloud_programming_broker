from accounting_service.domain.events.invoice_created import InvoiceCreatedEvent
from accounting_service.infrastructure.config.settings import Config
from accounting_service.infrastructure.messaging.event_bus import RabbitMQEventBus


class InvoiceCreatedEventPublisher:
    def __init__(self, event_bus: RabbitMQEventBus):
        self.event_bus = event_bus

    def publish(self, event: InvoiceCreatedEvent):
        self.event_bus.publish(event, exchange_type="direct", routing_key=Config.INVOICE_CREATED_ROUTING_KEY)
