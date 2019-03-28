# XUEQIU scraper for news

import requests
import json
import pymongo
import datetime
import time
import sys

CATEGORY_TO_ID = {
    "hkstocks": 102,
    "headlines": -1,
    "hushen": 105,
    "insurance": 110,
    "livenews": 6,
    "privatefund": 113,
    "property": 111,
}

def scrape(category):
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["bluefire"] # TODO: change DB name as needed
    now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    col_name = "xueqiu_{}_links_{}".format(category, now) 
    col = db[col_name]
    print("[!!] saving to column: {}".format(col_name))

    category_id = CATEGORY_TO_ID[category]
    endpoint = "https://xueqiu.com/v4/statuses/public_timeline_by_category.json?since_id=-1&count=15&category={}".format(category_id)

    next_max_id = -1
    while True:
        target = "{}&max_id={}".format(endpoint, next_max_id)
        print("[i] accessing {}".format(target))

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
            "Cookie": "_ga=GA1.2.1831851797.1552318131; device_id=fdac4e98e251135f1d9358c29c86f6f5; s=fi11i3vu0x; xq_a_token=7cf22354ec70fa7145e2c21aba5d4b456d58c2c5; xq_a_token.sig=kJw_N_lCztPdp2wWbx872xuHbn8; xq_r_token=d98947b3c6a584ed8e8ca297e4c928bbb0cfca39; xq_r_token.sig=xjRfXSpvjWBwQ7vhTyfZBquFrYk; u=901553682886892"
        }
        resp = requests.get(target, headers=headers)

        try:
            resp_json = json.loads(resp.text)
        except:
            # TODO: make this more robust/more controlled
            print("[info] encountered an error in scraping more links")
            print("[info] target: " + target)
            print(resp.text)
            break

        for item in resp_json["list"]:
            iteminfo = json.loads(item["data"])
            id_ = iteminfo["id"]
            try:
                title = iteminfo["title"]
                desc = iteminfo["description"]
            except:
                title = "N/A"
                desc = "N/A"
            
            try:
                content = iteminfo["text"]
            except:
                content = "N/A"
            
            link = iteminfo["target"]
            created_at = iteminfo["created_at"]
            view_count = iteminfo["view_count"]

            itemdict = {
                "article_id": id_,
                "title": title,
                "text_content": content,
                "link": link,
                "desc": desc,
                "created_at": created_at,
                "view_count": view_count
            }

            time_fmtd = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(int(created_at / 1000)))
            print("[i] time: {} / id: {} / link: {}".format(time_fmtd, id_, link))

            # Saves to the mongodb
            col.insert_one(itemdict)
        
        next_max_id = int(resp_json["next_max_id"])

        if next_max_id == -1:
            break

        time.sleep(1.5)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python xueqiu_link_scraper.py [category]")
        quit()
    
    category = sys.argv[1]
    print("[i] scraping category: {}".format(category))
    scrape(category)
    print("[i] done")
