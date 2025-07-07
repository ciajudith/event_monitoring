import json
from datetime import datetime


class Event:
    def __init__(
            self,
            timestamp: datetime,
            level: str,
            node: str,
            component: str,
            ids: str,
            message: str,
            event_id: str,
            template: str
    ):
        self.timestamp = timestamp
        self.level = level
        self.node = node
        self.component = component
        self.ids = ids
        self.message = message
        self.event_id = event_id
        self.template = template

    @classmethod
    def from_json(cls, json_str: str):
        data = json.loads(json_str)
        ts = data["timestamp"].replace("Z", "+00:00")
        timestamp = datetime.fromisoformat(ts)
        return cls(
            timestamp=timestamp,
            level=data.get("level"),
            node=data.get("node"),
            component=data.get("component"),
            ids=data.get("id"),
            message=data.get("message"),
            event_id=data.get("event_id"),
            template=data.get("template")
        )
