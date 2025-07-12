from collections import deque
from datetime import timedelta
from typing import Optional, Dict, Any, List

from src.models.alert import Alert
from src.models.event import Event


class EventAnalyzer:
    """
    Classe pour analyser les événements et générer des alertes basées sur des seuils de temps et de niveau.
    """
    def __init__(self, window_seconds: int = 30, threshold: int = 3):
        """
        Initialise l'analyseur d'événements.
        :param window_seconds:
        :param threshold:
        """
        self.window = timedelta(seconds=window_seconds)
        self.threshold = threshold
        self.critical_events: deque[Event] = deque()
        self.alerts: List[Alert] = []
        self.total_events: int = 0
        self.level_counts: Dict[str, int] = {}

    def feed(self, event: Event) -> Optional[Alert]:
        """
        Traite un événement et génère une alerte si les conditions sont remplies.
        Conditions pour générer une alerte :
        - Au moins `threshold` événements de niveau "CRITICAL" ou "ERROR" dans la fenêtre de temps définie.
        - Les événements doivent être dans la fenêtre de temps définie par `window_seconds`.
        :param event:
        :return:
        """
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
        """
        Retourne les statistiques de l'analyseur d'événements.
        :return:
        """
        return {
            "total_events": self.total_events,
            "level_counts": self.level_counts,
            "alerts": [a.to_dict() for a in self.alerts]
        }
