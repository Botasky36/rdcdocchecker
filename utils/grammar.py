import language_tool_python

def check_grammar(text):
    tool = language_tool_python.LanguageTool('en-US')  # เปลี่ยนเป็น 'th' หากใช้ภาษาไทย
    matches = tool.check(text)
    return f"พบข้อผิดพลาด {len(matches)} จุด", matches