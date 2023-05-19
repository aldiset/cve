import requests

#set host
host = "http://127.0.0.1:9999"

def get(cve_id, lang):
    endpoint = f"/api/vuln/cve/{cve_id}"
    url = host + endpoint

    params = {
        "cve_id": cve_id,
        "lang": lang #you can selected other language
    }
    response = requests.get(url=url, params=params)
    return response.json()

data = get(cve_id="CVE-2022-21664",lang="id")