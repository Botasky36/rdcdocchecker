import language_tool_python

def check_grammar(text):
    tool = language_tool_python.LanguageToolPublicAPI('en-US')
    
    if not text.strip():
        return 0, []

    if len(text) > 10000:
        text = text[:10000]

    matches = tool.check(text)
    return len(matches), matches
