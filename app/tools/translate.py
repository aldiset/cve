from googletrans import Translator

class TranslateText():
    @classmethod
    async def translate_text(self,lang: str, text: str = None):
        try:
            if text is not None:
                translator = Translator()
                translate = translator.translate(text=text, src="en", dest=lang)
                return translate.text 
            return "null"
        except Exception as e:
            print("=====")
            print(e)
            print("+++++")
            return "null"