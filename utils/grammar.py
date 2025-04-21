import language_tool_python
from pythainlp.spell import correct
from pythainlp.tokenize import word_tokenize
import re

# ตรวจจับภาษาอัตโนมัติ
def detect_language(text):
    thai_chars = len(re.findall(r'[ก-๙]', text))
    english_chars = len(re.findall(r'[a-zA-Z]', text))
    return 'th' if thai_chars > english_chars else 'en'

# ตรวจไวยากรณ์/คำผิด ภาษาไทยและอังกฤษ

def check_grammar(text):
    lang = detect_language(text)
    results = []

    if lang == 'en':
        tool = language_tool_python.LanguageTool('en-US')
        matches = tool.check(text)
        for m in matches:
            results.append({
                'error_text': text[m.offset : m.offset + m.errorLength],
                'suggestions': m.replacements,
                'message': m.message,
                'offset': m.offset
            })
        return f"🔤 ภาษาอังกฤษ: พบ {len(results)} ข้อผิดพลาด", results

    else:  # ภาษาไทย
        words = word_tokenize(text, engine='newmm')
        for word in words:
            if re.search(r'[ก-๙]', word):
                corrected = correct(word)
                if word != corrected:
                    results.append({
                        'error_text': word,
                        'suggestions': [corrected],
                        'message': "คำนี้อาจสะกดผิด"
                    })
        return f"🔤 ภาษาไทย: พบ {len(results)} คำที่อาจสะกดผิด", results
