import requests

#set host
host = "http://127.0.0.1:9999"

def get(cwe_id, lang):
    endpoint = f"/api/vuln/cwe/{cwe_id}"
    url = host + endpoint

    params = {
        "cwe_id": cwe_id,
        "lang": lang #you can selected other language
    }
    response = requests.get(url=url, params=params)
    return response.json()

get(cwe_id="CWE-12",lang="id")