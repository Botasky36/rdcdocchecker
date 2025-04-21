import re

def check_format(text): 
    required_sections = ["บทคัดย่อ", "บทนำ", "วิธีวิจัย", "ผลการวิจัย", "สรุป", "บรรณานุกรม"]
    report = {}
    text_lower = text.lower()
    for section in required_sections:
        pattern = rf"{section.lower()}"
        found = re.search(pattern, text_lower)
        report[section] = "✔️ พบ" if found else "❌ ไม่พบ"
    return report
