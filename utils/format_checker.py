def check_format(text):
    required_sections = ["บทคัดย่อ", "บทนำ", "วิธีวิจัย", "ผลการวิจัย", "สรุป", "บรรณานุกรม"]
    report = {}
    for section in required_sections:
        report[section] = "✔️ พบ" if section in text else "❌ ไม่พบ"
    return report