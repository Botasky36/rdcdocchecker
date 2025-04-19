from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
import base64

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
        for item in grammar_results[:10]:  # แสดง 10 รายการ
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