import pandas as pd
from fpdf import FPDF
from pybtex.database import BibliographyData, Entry

def generate_pdf_report(report_data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, txt=report_data["title"], ln=True, align="C")
    
    pdf.set_font("Arial", "", 12)
    pdf.cell(200, 10, txt=f"Date: {pd.Timestamp.now().strftime('%Y-%m-%d')}", ln=True, align="L")
    pdf.ln(10)

    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, txt="Abstract", ln=True, align="L")
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 5, report_data["abstract"])
    pdf.ln(5)

    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, txt="Key Findings", ln=True, align="L")
    pdf.set_font("Arial", "", 12)
    for finding in report_data["findings"]:
        pdf.multi_cell(0, 5, f"- {finding}")

    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, txt="References", ln=True, align="L")
    pdf.set_font("Arial", "", 10)
    for ref in report_data["references"]:
        pdf.multi_cell(0, 5, ref)

    return pdf.output(dest='S').encode('latin1')

def generate_citation(title, url):
    return BibliographyData({
        "ref": Entry("misc", fields={"title": title, "howpublished": url})
    }).to_string("bibtex")
