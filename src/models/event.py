import json
from datetime import datetime


class Event:
    """
    Représente un événement enregistré dans le système.
    """
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
        """
        Crée une instance d'Event à partir d'une chaîne JSON.
        :param json_str: str
        :return: Event
        """
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
    def to_dict(self) -> dict:
        """
        Convertit l'événement en dictionnaire pour la sérialisation JSON.
        :return: dict
        """
        return {
            "timestamp": self.timestamp.isoformat(),
            "level": self.level,
            "node": self.node,
            "component": self.component,
            "id": self.ids,
            "message": self.message,
            "event_id": self.event_id,
            "template": self.template
        }
