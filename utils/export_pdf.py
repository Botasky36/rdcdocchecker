from fpdf import FPDF
from io import BytesIO
import base64
import streamlit as st

def export_report_streamlit(text_dict):
    # สร้าง PDF ลงใน buffer
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="ผลการตรวจสอบเอกสารวิจัย", ln=True, align='C')

    for section, content in text_dict.items():
        pdf.ln(8)
        pdf.set_font("Arial", style="B", size=12)
        pdf.cell(200, 10, txt=section, ln=True)
        pdf.set_font("Arial", size=11)

        text = str(content)
        lines = text.split('\n')
        for line in lines:
            pdf.multi_cell(0, 10, txt=line)

    # แปลงเป็น BytesIO
    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)

    # แปลงเป็น base64
    b64 = base64.b64encode(buffer.read()).decode()
    href = f'<a href="data:application/pdf;base64,{b64}" download="report.pdf">📥 ดาวน์โหลด PDF รายงาน</a>'
    st.markdown(href, unsafe_allow_html=True)
