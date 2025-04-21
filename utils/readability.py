import textstat
from pythainlp.tokenize import word_tokenize, sent_tokenize
import re

def detect_language(text):
    thai_chars = len(re.findall(r'[ก-๙]', text))
    eng_chars = len(re.findall(r'[a-zA-Z]', text))
    return 'th' if thai_chars > eng_chars else 'en'

def check_readability(text):
    lang = detect_language(text)
    
    if lang == 'en':
        return {
            "ภาษา": "อังกฤษ",
            "Flesch Reading Ease": round(textstat.flesch_reading_ease(text), 2),
            "Text Standard": textstat.text_standard(text)
        }
    else:
        words = word_tokenize(text)
        sents = sent_tokenize(text)
        return {
            "ภาษา": "ไทย",
            "จำนวนคำ": len(words),
            "จำนวนประโยค": len(sents),
            "เฉลี่ยคำต่อประโยค": round(len(words)/len(sents), 2) if sents else 0
        }
0
