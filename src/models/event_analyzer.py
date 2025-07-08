from collections import deque
from datetime import timedelta
from typing import Optional, Dict, Any, List

from src.models.alert import Alert
from src.models.event import Event


class EventAnalyzer:
    def __init__(self, window_seconds: int = 30, threshold: int = 3):
        self.window = timedelta(seconds=window_seconds)
        self.threshold = threshold
        self.critical_events: deque[Event] = deque()
        self.alerts: List[Alert] = []
        self.total_events: int = 0
        self.level_counts: Dict[str, int] = {}

    def feed(self, event: Event) -> Optional[Alert]:
        self.total_events += 1
        self.level_counts[event.level] = self.level_counts.get(event.level, 0) + 1
        if event.level == "CRITICAL" or event.level == "ERROR":
            self.critical_events.append(event)
            while self.critical_events and (event.timestamp - self.critical_events[0].timestamp) > self.window:
                self.critical_events.popleft()
            if len(self.critical_events) >= self.threshold:
                alert = Alert(
                    start=self.critical_events[0].timestamp,
                    end=event.timestamp,
                    count=len(self.critical_events),
                    events=list(self.critical_events)
                )
                self.alerts.append(alert)
                self.critical_events.clear()
                return alert
        else :
            self.critical_events.clear()
        return None

    def stats(self) -> Dict[str, Any]:
        return {
            "total_events": self.total_events,
            "level_counts": self.level_counts,
            "alerts": [a.to_dict() for a in self.alerts]
        }
