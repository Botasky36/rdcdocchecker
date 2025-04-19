from fpdf import FPDF

def export_report(text_dict, filename="report.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="ผลการตรวจสอบเอกสารวิจัย", ln=True, align='C')

    for section, content in text_dict.items():
        pdf.ln(10)
        pdf.set_font("Arial", style="B", size=12)
        pdf.cell(200, 10, txt=section, ln=True)
        pdf.set_font("Arial", size=11)
        lines = content.split('\n')
        for line in lines:
            pdf.multi_cell(0, 10, txt=line)

    pdf.output(filename)