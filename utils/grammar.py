import language_tool_python

def check_grammar(text):
    tool = language_tool_python.LanguageToolPublicAPI('en-US')
    matches = tool.check(text)
    return f"พบข้อผิดพลาด {len(matches)} จุด", matches
