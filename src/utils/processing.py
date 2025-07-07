import asyncio
import json
from datetime import datetime
from pathlib import Path

from fpdf import FPDF

from src.models.event import Event
from src.models.event_analyzer import EventAnalyzer
from src.models.event_logger import EventLogger
from src.utils.plot_generation import plot_level_counts

# Constantes pour les fichiers de sortie
OUTPUT_DIR = Path("outputs")
ALERT_FILE = OUTPUT_DIR / "alerts.json"
REPORT_FILE = OUTPUT_DIR / "report.pdf"
PLOT_FILE   = OUTPUT_DIR / "stats.png"


analyzer = EventAnalyzer()
logger = EventLogger(alert_file=str(ALERT_FILE))

async def process_logs(log_path: str = "src/input/events.log", delay: float = 2.0):
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
    stats = analyzer.stats()
    plot_level_counts(analyzer.stats()["level_counts"], save_path=PLOT_FILE, show=False)
    # PDF creation
    pdf = FPDF()
    pdf.set_auto_page_break(margin=15, auto=True)
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Rapport de traitement des logs", ln=True, align="C")
    pdf.ln(5)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, f"Date : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.ln(5)

    # Statistiques
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 8, "Statistiques globales :", ln=True)
    pdf.ln(3)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 6, f"Nombre total des évenements                : {stats['total_events']}\n", ln=True)
    pdf.cell(0, 6, f"Nombre total des évenements critiques : {stats['level_counts'].get('CRITICAL', 0)+stats['level_counts'].get('ERROR', 0)}\n", ln=True)
    pdf.cell(0, 6, f"Nombres d'alerte(s) détectée(s)             : {len(stats['alerts'])}\n", ln=True)
    pdf.ln(5)

    # Alert details
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 8, "Détails des alertes :", ln=True)
    pdf.ln(3)
    pdf.set_font("Arial", "", 12)
    for a in stats["alerts"]:
        start_dt = datetime.fromisoformat(a["start"])
        end_dt = datetime.fromisoformat(a["end"])

        fmt = "%d/%m/%Y %H:%M:%S"

        start_str = start_dt.strftime(fmt)
        end_str = end_dt.strftime(fmt)

        pdf.multi_cell(0, 6, f"- Début : {start_str}  Fin : {end_str}  Nombre : {a['count']}")
    pdf.ln(10)

    # Histogram
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 8, "Histogramme des niveaux :", ln=True)
    pdf.image(str(PLOT_FILE), x=30, w=150)
    pdf.ln(10)

    pdf.output(str(REPORT_FILE))
    return REPORT_FILE

def get_alerts():
    if not ALERT_FILE.exists():
        return []
    return json.loads(ALERT_FILE.read_text(encoding="utf-8"))


def get_level_counts():
    return analyzer.level_counts

