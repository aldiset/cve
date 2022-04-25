import requests

#set host
host = "http://127.0.0.1:9999"

def get(cve_id, lang):
    endpoint = f"/api/vuln/generate/{cve_id}/pdf"
    url = host + endpoint

    params = {
        "cve_id": cve_id,
        "lang": lang #you can selected other language
    }
    response = requests.get(url=url, params=params, allow_redirects=True, stream=True)

    if response.status_code == 200:
        #write response file
        filename = (response.headers.get("content-disposition")).split('"')
        with open(filename[1], "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        return filename
    return False

data = get(cve_id="CVE-2022-21664",lang="id")
print(data)