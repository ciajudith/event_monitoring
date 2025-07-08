import asyncio
import json
import traceback
from datetime import datetime
from pathlib import Path

from fpdf import FPDF

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


analyzer = EventAnalyzer()
logger = EventLogger(alert_file=str(ALERT_FILE))

async def process_logs(log_path: str = "input/events.log", delay: float = 2.0):
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
                traceback.print_exc()
            await asyncio.sleep(delay)
    return analyzer


def generate_report() -> Path:
    stats = analyzer.stats()
    plot_level_counts(analyzer.stats()["level_counts"], save_path=PLOT_FILE, show=False)
    report_path = build_pdf_report(stats, PLOT_FILE, REPORT_FILE)
    return report_path

def get_alerts():
    if not ALERT_FILE.exists():
        return []
    return json.loads(ALERT_FILE.read_text(encoding="utf-8"))


def get_level_counts():
    return analyzer.level_counts

