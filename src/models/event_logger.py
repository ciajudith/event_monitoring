import logging
import json
from pathlib import Path
from  src.models.event_analyzer import Alert

class EventLogger:
    """
    Classe pour enregistrer les événements et les alertes dans un fichier JSON (alerts.json).
    Cette classe gère également la journalisation des messages d'information, d'avertissement, d'erreur et critique.
    """
    def __init__(self, alert_file: str = "outputs/alerts.json", log_level: int = logging.INFO):
        self.logger = logging.getLogger("EventMonitor")
        self.logger.setLevel(log_level)
        handler = logging.StreamHandler()
        fmt = logging.Formatter("[%(levelname)s] %(message)s")
        handler.setFormatter(fmt)
        if not self.logger.handlers:
            self.logger.addHandler(handler)

        self.alert_path = Path(alert_file)
        self.alert_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.alert_path.exists():
            self.alert_path.write_text("[]", encoding="utf-8")

    def info(self, msg: str):
        self.logger.info(msg)

    def warning(self, msg: str):
        self.logger.warning(msg)

    def error(self, msg: str):
        self.logger.error(msg)

    def critical(self, msg: str):
        self.logger.critical(msg)

    def record(self, alert: Alert):
        data = json.loads(self.alert_path.read_text(encoding="utf-8"))
        data.append(alert.to_dict())
        self.alert_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        self.logger.critical(f"Alerte enregistrée : ({alert.count} événements)")