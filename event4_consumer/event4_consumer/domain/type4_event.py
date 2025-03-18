import json
from dataclasses import dataclass

from ..domain.type_event import TypeEvent


@dataclass
class Type4Event(TypeEvent):

    def to_json(self) -> str:
        return json.dumps({
            "event_id": self.event_id,
            "timestamp": self.timestamp
        })

    @staticmethod
    def from_json(data: str):
        obj = json.loads(data)
        return Type4Event(event_id=obj["event_id"], timestamp=obj["timestamp"])