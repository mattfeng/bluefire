import requests
import json

def get_recent_news():
    endpoint = "http://app.cnstock.com/api/xcx/kx?&colunm=szkx&page={}&num=15"

    pagenum = 1
    while True:
        resp = requests.get(endpoint.format(pagenum))
        resp_json = json.loads(resp.text)
        print(resp_json)

        if resp_json["error"] != 0:
            break
        
        pagenum += 1

if __name__ == "__main__":
    get_recent_news()