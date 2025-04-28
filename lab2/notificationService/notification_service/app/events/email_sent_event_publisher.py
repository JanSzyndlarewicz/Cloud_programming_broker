from notification_service.domain.events.email_sent import EmailSentEvent
from notification_service.infrastructure.config import Config
from notification_service.infrastructure.event_bus.rabbitmq_event_bus import RabbitMQEventBus


class EmailSentEventPublisher:
    def __init__(self, event_bus: RabbitMQEventBus):
        self.event_bus = event_bus

    def publish(self, event: EmailSentEvent):
        self.event_bus.publish(event, exchange_type="direct", routing_key=Config.EMAIL_SENT_ROUTING_KEY)
