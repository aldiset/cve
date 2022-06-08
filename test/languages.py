import requests

#set host
host = "http://127.0.0.1:9999"

def get():
    endpoint = f"/api/vuln/languages"
    url = host + endpoint

    response = requests.get(url=url)
    return response.json()

data = get()