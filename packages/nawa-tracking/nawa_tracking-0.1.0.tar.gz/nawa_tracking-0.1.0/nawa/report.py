from fpdf import FPDF
from datetime import datetime

def build_pdf(result: dict) -> str:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)

    pdf.cell(200, 10, txt="NAWA Face-Match Report", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Name: {result.get('name', 'Unknown')}", ln=True)
    pdf.cell(200, 10, txt=f"Confidence: {result.get('confidence', 0.0)} %", ln=True)
    pdf.cell(200, 10, txt=f"Latency: {int(result.get('latency_ms', 0))} ms", ln=True)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pdf.cell(200, 10, txt=f"Timestamp: {now}", ln=True)

    path = "nawa_report.pdf"
    pdf.output(path)

    return path

