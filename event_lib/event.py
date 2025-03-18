from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Event(ABC):
    event_id: str
    timestamp: float

    @abstractmethod
    def to_json(self) -> str:
        pass

    @staticmethod
    @abstractmethod
    def from_json(data: str):
        pass