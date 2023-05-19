import requests

#set host
host = "http://127.0.0.1:9999"

def get(capec_id, lang):
    endpoint = "/api/vuln/capec/{capec_id}"
    url = host + endpoint

    params = {
        "lang": lang #you can selected other language
    }
    response = requests.get(url=url, params=params)
    return response.json()