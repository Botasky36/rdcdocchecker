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

# ฟังก์ชันสร้าง PDF รายงาน
def generate_pdf_report(grammar_results, format_results, readability_results, structure_results):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    x = 50
    y = height - 50

    def write_line(text, indent=0, font_size=11):
        nonlocal y
        c.setFont("Helvetica", font_size)
        c.drawString(x + indent, y, text)
        y -= 18
        if y < 50:
            c.showPage()
            y = height - 50

    write_line("ผลการตรวจสอบเอกสารวิจัย", font_size=16)
    write_line("-----------------------------------------")

    write_line("🔤 ตรวจไวยากรณ์และการสะกด")
    if grammar_results:
        for item in grammar_results[:10]:
            write_line(f"- ข้อความ: {item['error_text']}", indent=20)
            write_line(f"  ข้อเสนอแนะ: {', '.join(item['suggestions'])}", indent=40)
            write_line(f"  คำอธิบาย: {item['message']}", indent=40)
    else:
        write_line("✅ ไม่พบข้อผิดพลาด")

    write_line("")
    write_line("📐 ตรวจรูปแบบเอกสาร")
    for section, result in format_results.items():
        write_line(f"- {section}: {result}", indent=20)

    write_line("")
    write_line("📊 ตรวจคุณภาพการอ่าน")
    for k, v in readability_results.items():
        write_line(f"- {k}: {v}", indent=20)

    write_line("")
    write_line("🧠 สรุปองค์ประกอบเอกสาร")
    for title, content in structure_results.items():
        write_line(f"{title}:", indent=20)
        write_line(content[:300] + "...", indent=40)

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

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
        count, matches = check_grammar(cleaned_text)
        st.write(f"พบ {count} ข้อผิดพลาด")
        for m in matches[:5]:
            st.markdown(f"- ❗ {m.message} (ตำแหน่ง: {m.offset})")

    # แปลง matches เป็น list ที่ใช้ใน PDF
    grammar_data = []
    for m in matches:
        grammar_data.append({
            'error_text': cleaned_text[m.offset:m.offset + m.errorLength],
            'suggestions': m.replacements,
            'message': m.message
        })

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

    # ปุ่มดาวน์โหลด PDF
    if st.button("📄 ดาวน์โหลดผลการตรวจเป็น PDF"):
        pdf_buffer = generate_pdf_report(grammar_data, format_result, readability, summary)
        b64 = base64.b64encode(pdf_buffer.read()).decode()
        href = f'<a href="data:application/pdf;base64,{b64}" download="report.pdf">📥 คลิกเพื่อดาวน์โหลดรายงาน</a>'
        st.markdown(href, unsafe_allow_html=True)
    # 🧾 ข้อมูลการติดต่อผู้พัฒนา
# -------------------------------
st.markdown("""
<hr style="border:1px solid #003366; margin-top:40px; margin-bottom:10px">
<div style="text-align: center; color: #003366; font-size: 14px;">
    📞 ติดต่อสอบถามปัญหาการใช้งานระบบ<br>
    ผู้พัฒนา: สำนักงานวิจัย ศูนย์วิจัยพัฒนาวิทยาศาสตร์เทคโนโลยีการบินและอวกาศ กองทัพอากาศ<br>
    อีเมล: <a href="mailto:piyapan_th@rtaf.mi.th">piyapan_th@rtaf.mi.th</a><br>
    โทรศัพท์: 02-534-4849 ต่อ 12345
</div>
""", unsafe_allow_html=True)