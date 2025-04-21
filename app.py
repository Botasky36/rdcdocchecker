import streamlit as st
from utils.reader import extract_text_from_pdf, extract_text_from_docx
from utils.grammar import check_grammar
from utils.format_checker import check_format
from utils.readability import check_readability
from utils.structure_summary import summarize_structure

import re
from PIL import Image
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import base64
from fpdf import FPDF

# กำหนดสไตล์หน้า
st.set_page_config(page_title="Research Document Checker", layout="wide")

# เพิ่มสไตล์ CSS สำหรับกองทัพอากาศ
st.markdown("""
    <style>
        .stApp {
            background-color: #e6f0fa;
        }
        h1, h2, h3, h4 {
            color: #003366;
        }
        .stButton > button {
            background-color: #005580;
            color: white;
            border-radius: 8px;
            font-weight: bold;
        }
        details summary {
            background-color: #cce0f5;
            color: #003366;
            padding: 10px;
            font-size: 18px;
            border-radius: 5px;
        }
        .stMarkdown, .stText, .stSubheader {
            color: #002147;
        }
    </style>
""", unsafe_allow_html=True)

# เพิ่มโลโก้ศวอ.ทอ.
logo = Image.open("logo_rtaf.png")
st.image(logo, width=100)

# หัวข้อหลัก
st.title("📘 ระบบตรวจสอบเอกสารวิจัย")
st.subheader("ศูนย์วิจัยพัฒนาวิทยาศาสตร์เทคโนโลยีการบินเเละอวกาศกองทัพอากาศ")

# ฟังก์ชันลบช่องว่างซ้ำ
def remove_extra_spaces(text):
    return re.sub(r'\s{2,}', ' ', text)

# ฟังก์ชัน export PDF ผ่าน FPDF + Streamlit
def export_report_streamlit(text_dict):
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

    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)

    b64 = base64.b64encode(buffer.read()).decode()
    href = f'<a href="data:application/pdf;base64,{b64}" download="report.pdf">📥 ดาวน์โหลด PDF รายงาน</a>'
    st.markdown(href, unsafe_allow_html=True)

# อัปโหลดไฟล์
uploaded_file = st.file_uploader("อัปโหลดไฟล์ PDF หรือ DOCX", type=["pdf", "docx"])

if uploaded_file:
    if uploaded_file.name.endswith(".pdf"):
        text = extract_text_from_pdf(uploaded_file)
    else:
        text = extract_text_from_docx(uploaded_file)

    st.success("✅ อัปโหลดสำเร็จและอ่านไฟล์เรียบร้อยแล้ว")

    cleaned_text = remove_extra_spaces(text)

    with st.expander("🔤 ตรวจไวยากรณ์และการสะกด"):
        msg, matches = check_grammar(cleaned_text)
        st.write(msg)
        for m in matches[:5]:
            st.markdown(f"- ❗ {m['error_text']} → {', '.join(m['suggestions'])} ({m['message']})")

    grammar_data = matches

    with st.expander("📐 ตรวจรูปแบบเอกสาร"):
        format_result = check_format(cleaned_text)
        for section, result in format_result.items():
            st.write(f"- {section}: {result}")

    with st.expander("📊 ตรวจคุณภาพการอ่าน"):
        readability = check_readability(cleaned_text)
        for k, v in readability.items():
            st.write(f"{k}: {v}")

    with st.expander("🧠 สรุปองค์ประกอบเอกสาร"):
        summary = summarize_structure(cleaned_text)
        for title, content in summary.items():
            st.subheader(title)
            st.write(content[:500] + "..." if len(content) > 500 else content)

    # สร้างรายงานสรุปแบบ dict
    summary_data = {
        "🔤 ตรวจคำผิด": msg + "\n" + "\n".join([
            f"- {item['error_text']} → {', '.join(item['suggestions'])}" for item in grammar_data[:10]
        ]),
        "📐 รูปแบบเอกสาร": "\n".join([f"{k}: {v}" for k, v in format_result.items()]),
        "📊 ความสามารถในการอ่าน": "\n".join([f"{k}: {v}" for k, v in readability.items()]),
        "🧠 สรุปองค์ประกอบ": "\n".join([f"{k}: {v[:150]}..." for k, v in summary.items()])
    }

    export_report_streamlit(summary_data)

# 🧾 ข้อมูลการติดต่อผู้พัฒนา
st.markdown("""
<hr style="border:1px solid #003366; margin-top:40px; margin-bottom:10px">
<div style="text-align: center; color: #003366; font-size: 14px;">
    📞 ติดต่อสอบถามปัญหาการใช้งานระบบ<br>
    ผู้พัฒนา: สำนักงานวิจัย ศูนย์วิจัยพัฒนาวิทยาศาสตร์เทคโนโลยีการบินและอวกาศ กองทัพอากาศ<br>
    อีเมล: <a href=\"mailto:piyapan_th@rtaf.mi.th\">piyapan_th@rtaf.mi.th</a><br>
    โทรศัพท์: 02-534-4849 ต่อ 12345
</div>
""", unsafe_allow_html=True)

