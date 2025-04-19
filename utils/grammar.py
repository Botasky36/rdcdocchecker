from pythainlp.spell import NorvigSpellChecker
from pythainlp.tokenize import word_tokenize
import language_tool_python

spell_checker = NorvigSpellChecker()

def check_thai_spelling(text):
    words = word_tokenize(text, engine="newmm")
    mistakes = []

    for word in words:
        if not spell_checker.correct(word):
            suggestions = spell_checker.suggest(word)
            if suggestions and suggestions[0] != word:
                mistakes.append({
                    'error_text': word,
                    'suggestions': suggestions,
                    'message': "อาจสะกดผิด"
                })
    return len(mistakes), mistakes
