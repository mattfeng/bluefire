import requests
import json
import pymongo
import time
import datetime

def get_recent_news_links():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["bluefire"]
    now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    col = db["cnstock_{}".format(now)]

    endpoint = "http://app.cnstock.com/api/xcx/kx?&colunm=szkx&page={}&num=15"

    pagenum = 1
    while True:
        resp = requests.get(endpoint.format(pagenum))
        resp_json = json.loads(resp.text)
        print(resp_json)

        if resp_json["error"] != 0:
            break

        for item in resp_json["item"]:
            col.insert(item)
        
        pagenum += 1
        time.sleep(1)

if __name__ == "__main__":
    get_recent_news_links()