from datetime import datetime
from pathlib import Path
from fpdf import FPDF


def build_pdf_report(stats: dict, image_path: Path, output_path: Path) -> Path:
    pdf = FPDF()
    pdf.set_auto_page_break(margin=15, auto=True)
    pdf.add_page()
    pdf.add_font("NotoEmoji", "", "src/fonts/NotoEmoji-Regular.ttf", uni=True)
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Rapport de traitement des logs", ln=True, align="C")
    pdf.ln(5)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, f"Généré le : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.ln(5)

    card_data = [
        ("\u26A0", "Total Events", stats['total_events'], (220, 220, 220)),
        ("\u26D4", "Critical Events", stats['level_counts'].get('CRITICAL', 0), (255, 204, 204)),
        ("\u26A1", "Error Events", stats['level_counts'].get('ERROR', 0), (255, 229, 204)),
        ("\U0001F6A8", "Alertes", len(stats['alerts']), (204, 229, 255)),
    ]
    x, y, w, h = 10, pdf.get_y(), 45, 30
    spacing = 5
    for i, (icon, label, value, color) in enumerate(card_data):
        card_x = x + i * (w + spacing)
        pdf.set_xy(card_x, y)
        pdf.set_fill_color(*color)
        pdf.set_draw_color(100, 100, 100)  # dark border
        pdf.rect(card_x, y, w, h, style='DF')  # Draw filled rectangle with border
        pdf.set_xy(card_x, y + 4)
        pdf.set_font("NotoEmoji", "", 22)
        pdf.cell(w, 10, icon, align="C", ln=2)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(w, 6, label, align="C", ln=2)
        pdf.set_font("Arial", "", 14)
        pdf.cell(w, 6, str(value), align="C")
    pdf.ln(8)
    pdf.ln(10)
    # Statistiques
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 8, "Statistiques globales :", ln=True)
    pdf.ln(3)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 6, f"Nombre total des évenements                : {stats['total_events']}\n", ln=True)
    pdf.cell(0, 6, f"Nombre total des évenements critiques : {stats['level_counts'].get('CRITICAL', 0)+stats['level_counts'].get('ERROR', 0)}\n", ln=True)
    pdf.cell(0, 6, f"Nombres d'alerte(s) détectée(s)             : {len(stats['alerts'])}\n", ln=True)
    pdf.ln(10)

    # Alertes
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 8, "Détails des alertes :", ln=True)
    pdf.ln(3)
    pdf.set_font("Arial", "", 12)
    fmt = "%d/%m/%Y %H:%M:%S"
    for idx, a in enumerate(stats["alerts"], 1):
        start_dt = datetime.fromisoformat(a["start"])
        end_dt = datetime.fromisoformat(a["end"])
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 6,
                 f"Alerte {idx} : Début : {start_dt.strftime(fmt)}  Fin : {end_dt.strftime(fmt)}  Nombre : {a['count']}",
                 ln=True)
        pdf.ln(3)
        pdf.set_font("Arial", "", 11)
        pdf.set_fill_color(230, 230, 250)
        pdf.cell(50, 6, "Timestamp", 1, 0, "C", True)
        pdf.cell(45, 6, "Niveau", 1, 0, "C", True)
        pdf.cell(90, 6, "Message", 1, 1, "C", True)
        for ev in a["events"]:
            pdf.cell(50, 6, ev["timestamp"].replace("T", " ")[:19], 1, 0, "C")
            pdf.cell(45, 6, ev["level"], 1, 0, "C")
            msg = ev["message"][:40] + ("..." if len(ev["message"]) > 40 else "")
            pdf.cell(90, 6, msg, 1, 1, "C")
        pdf.ln(3)

    pdf.ln(10)

    # Histogramme
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 8, "Histogramme des niveaux :", ln=True)
    pdf.image(str(image_path), x=30, w=150)
    pdf.ln(10)

    pdf.output(str(output_path))
    return output_path
