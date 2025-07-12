import asyncio
import json
from pathlib import Path


from src.models.event import Event
from src.models.event_analyzer import EventAnalyzer
from src.models.event_logger import EventLogger
from src.utils.plot_generation import plot_level_counts
from src.utils.report_generation import build_pdf_report

# Constantes pour les fichiers de sortie
OUTPUT_DIR = Path("outputs")
ALERT_FILE = OUTPUT_DIR / "alerts.json"
REPORT_FILE = OUTPUT_DIR / "report.pdf"
PLOT_FILE   = OUTPUT_DIR / "stats.png"


analyzer = None
logger = None

async def process_logs(log_path: str = "input/events.log", delay: float = 2.0):
    """
    Fonction asynchrone pour traiter les logs d'événements.
    :param log_path: Chemin vers le fichier de logs à traiter.
    :param delay: Délai en secondes entre le traitement de chaque ligne de log.
    :return: L'instance de l'analyseur d'événements.
    """
    global analyzer, logger
    if analyzer is None:
        analyzer = EventAnalyzer()
    if logger is None:
        logger = EventLogger(alert_file=str(ALERT_FILE))
    OUTPUT_DIR.mkdir(exist_ok=True)
    if not ALERT_FILE.exists():
        ALERT_FILE.write_text("[]", encoding="utf-8")

    with open(log_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                event = Event.from_json(line)
                logger.info(f"{event.level} – {event.event_id} – {event.message}")
                alert = analyzer.feed(event)
                if alert:
                    logger.record(alert)
            except Exception as e:
                logger.error(f"Erreur lors du parsing : {e}")
            await asyncio.sleep(delay)
    return analyzer


def generate_report() -> Path:
    """
    Génère un rapport PDF à partir des statistiques de l'analyseur d'événements.
    """
    stats = analyzer.stats()
    plot_level_counts(analyzer.stats()["level_counts"], save_path=PLOT_FILE, show=False)
    report_path = build_pdf_report(stats, PLOT_FILE, REPORT_FILE)
    return report_path

def get_alerts():
    """
    Récupère les alertes enregistrées dans le fichier JSON.
    """
    if not ALERT_FILE.exists():
        return []
    return json.loads(ALERT_FILE.read_text(encoding="utf-8"))


def get_level_counts():
    """
    Récupère les comptes de niveaux d'événements de l'analyseur.
    """
    return analyzer.level_counts

