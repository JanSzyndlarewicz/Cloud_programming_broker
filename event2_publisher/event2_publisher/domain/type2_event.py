import json
from dataclasses import dataclass


@dataclass
class Type2Event:
    event_id: str
    timestamp: float

    def to_json(self) -> str:
        return json.dumps({
            "event_id": self.event_id,
            "timestamp": self.timestamp
        })

    @staticmethod
    def from_json(data: str):
        obj = json.loads(data)
        return Type2Event(event_id=obj["event_id"], timestamp=obj["timestamp"])
