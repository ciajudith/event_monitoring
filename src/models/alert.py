from typing import Dict, Any


class Alert:
    def __init__(self, start, end, count):
        self.start = start
        self.end = end
        self.count = count
        self.events = []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "start": self.start.isoformat(),
            "end": self.end.isoformat(),
            "count": self.count,
            "events": [event.to_dict() for event in self.events]
        }
