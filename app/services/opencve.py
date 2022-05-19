import requests

from app.tools.translate import TranslateText


host = "https://www.opencve.io/api"


class OpenCve:
    endpoints = {
        "CVE":host+"/cve/{}",
        "CWE":host+"/cwe/{}",
    }

    @classmethod
    async def get_cve_detail(cls, cve_id: str):
        url = cls.endpoints["CVE"].format(cve_id)
        response = requests.get(url=url, auth=("akarkode","4K4rk0d3"))
        
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, {}
    
    @classmethod
    async def get_cwe_detail(cls, cwe_id: str, lang: str):
        url = cls.endpoints["CWE"].format(cwe_id)
        response = requests.get(url=url, auth=("akarkode","4K4rk0d3"))
        
        if response.status_code == 200:
            data = response.json()
            description = await TranslateText.translate_text(lang=lang, text=data.get("description"))
            data.pop("description")
            data["description"] = description
            return True, data
        else:
            return False, {}