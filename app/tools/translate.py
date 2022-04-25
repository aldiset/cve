from googletrans import Translator

class TranslateText():
    @classmethod
    async def translate_text(self,lang: str, text: str = None):
        if text is not None:
            translator = Translator()
            translate = translator.translate(text=text, src="en", dest=lang)
            return translate.text
        return None