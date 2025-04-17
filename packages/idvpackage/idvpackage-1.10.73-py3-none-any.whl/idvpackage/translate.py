from googletrans import Translator
from deep_translator import GoogleTranslator

def translate_ar_to_en(text_to_translate):
    translated = GoogleTranslator('ar', 'en').translate(f"NAME: {text_to_translate}").upper()
    if "NAME: " in translated:
        translated = translated.replace(
            "NAME: ", "")

    return translated