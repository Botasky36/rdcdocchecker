import textstat

def check_readability(text):
    return {
        "การอ่านเข้าใจเนื้อหา คะเเนน": textstat.flesch_reading_ease(text),
        "คุณภาพเนื้อหา": textstat.text_standard(text)
    }