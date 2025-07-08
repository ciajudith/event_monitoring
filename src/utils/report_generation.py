from datetime import datetime
from pathlib import Path
from fpdf import FPDF


def build_pdf_report(stats: dict, image_path: Path, output_path: Path) -> Path:
    pdf = FPDF()
    pdf.set_auto_page_break(margin=15, auto=True)
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Rapport de traitement des logs", ln=True, align="C")
    pdf.ln(5)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, f"Généré le : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
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

    # Alertes
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 8, "Détails des alertes :", ln=True)
    pdf.ln(3)
    pdf.set_font("Arial", "", 12)
    fmt = "%d/%m/%Y %H:%M:%S"
    for a in stats["alerts"]:
        start_dt = datetime.fromisoformat(a["start"])
        end_dt = datetime.fromisoformat(a["end"])
        pdf.multi_cell(0, 6, f"- Début : {start_dt.strftime(fmt)}  Fin : {end_dt.strftime(fmt)}  Nombre : {a['count']}")

    pdf.ln(10)

    # Histogramme
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 8, "Histogramme des niveaux :", ln=True)
    pdf.image(str(image_path), x=30, w=150)
    pdf.ln(10)

    pdf.output(str(output_path))
    return output_path
