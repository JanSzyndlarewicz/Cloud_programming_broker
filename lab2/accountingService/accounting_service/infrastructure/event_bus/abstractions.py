from abc import ABC, abstractmethod
from typing import Any


class EventBus(ABC):
    @abstractmethod
    def publish(self, event: Any, routing_key: str):
        pass

    @abstractmethod
    def subscribe(self, queue: str, callback: callable, routing_key: str = None):
        pass
