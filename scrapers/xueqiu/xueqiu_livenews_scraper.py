import requests
import json
import pymongo
import datetime
import time

def scrape():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["bluefire"]
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    col = db["xueqiu_livenews_{}".format(now)]

    endpoint = "https://xueqiu.com/v4/statuses/public_timeline_by_category.json?since_id=-1&count=15&category=6"

    next_max_id = -1
    while True:
        target = "{}&max_id={}".format(endpoint, next_max_id)

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
            "Cookie": "_ga=GA1.2.1831851797.1552318131; device_id=fdac4e98e251135f1d9358c29c86f6f5; s=fi11i3vu0x; xq_a_token=81d45773abb1b366e832845c99c1c70dc9657551; xq_a_token.sig=8GjDWaPUPffpVUZFEG1Qw4rtM-U; xq_r_token=b9b80f015be55a28a155ffd7b95102c453a7273f; xq_r_token.sig=Xcs0PISsRDxf4ZvBdguYPn4t2oU; u=791553533010243"
        }
        resp = requests.get(target, headers=headers)

        resp_json = json.loads(resp.text)

        for item in resp_json["list"]:
            iteminfo = json.loads(item["data"])
            id_ = iteminfo["id"]
            content = iteminfo["text"]
            link = iteminfo["target"]
            createdate = iteminfo["created_at"]
            viewcount = iteminfo["view_count"]

            itemdict = {
                "article_id": id_,
                "text_content": content,
                "link": link,
                "created_on": createdate,
                "view_count": viewcount
            }

            print(link)

            # saves to the mongodb db=bluefire, collection=xueqiu_livenews_<datetime>
            col.insert_one(itemdict)
        
        next_max_id = int(resp_json["next_max_id"])

        if next_max_id == -1:
            break

        time.sleep(1.5)


if __name__ == "__main__":
    scrape()
