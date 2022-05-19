import requests
from app.tools.translate import TranslateText

host = 'https://cve.circl.lu/api/cve/'

class CirlLu:
    endpoints = {
        "CVE":host+"{}"
    }
    @classmethod
    async def get_cve_detail(cls,lang:str = None,cve_id: str = None ):
        url = cls.endpoints["CVE"].format(cve_id)
        response = requests.get(url=url)
        
        if response.status_code == 200:
            datas = response.json()
            capecs = datas.get("capec")
            if capecs is not None:
                capec_translate = []
                if lang not in [None,"en"]:
                    for capec in capecs:
                        capec_dict = {
                            'id': capec.get("id"),
                            'name': capec.get("name"),
                            'prerequisites': await TranslateText.translate_text(
                                            lang=lang, text = capec.get("prerequisites")),
                            'solutions' : await TranslateText.translate_text(
                                            lang=lang, text = capec.get("solutions")),
                            'summary' : await TranslateText.translate_text(
                                            lang = lang, text = capec.get("summary"))
                        }
                        capec_translate.append(capec_dict)
                    datas.pop("capec")
                    datas["capec"] = capec_translate
                else:
                    for capec in capecs:
                        capec.pop("related_weakness")
            else:
                datas["capec"]="Unknown"

            if lang not in [None,"en"]:
                summary = await TranslateText.translate_text(lang=lang, text = datas.get("summary"))
            else:
                summary = datas.get("summary")   

            datas.pop("summary")
            datas["description"] = summary

            remove_key = ["vulnerable_configuration","vulnerable_configuration_cpe_2_2","vulnerable_product"]
            for key in remove_key:
                if datas.get(key) is not None:
                    datas.pop(key)

            return True, datas
        else:
            return False, {}
