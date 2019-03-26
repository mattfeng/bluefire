import requests
import json

def scrape(category):
    endpoints = {
        "livenews": "https://xueqiu.com/v4/statuses/public_timeline_by_category.json?since_id=-1&count=15&category=6",
        "hushen": "https://xueqiu.com/v4/statuses/public_timeline_by_category.json?since_id=-1&count=10&category=105", # 沪深
        "toutiao": "https://xueqiu.com/v4/statuses/public_timeline_by_category.json?since_id=-1&count=10&category=-1",
        "tech": "https://xueqiu.com/v4/statuses/public_timeline_by_category.json?since_id=-1&count=10&category=115",
        "hkstocks": "https://xueqiu.com/v4/statuses/public_timeline_by_category.json?since_id=-1&count=10&category=102",
        "financialmgmt": "https://xueqiu.com/v4/statuses/public_timeline_by_category.json?since_id=-1&count=10&category=104",
        "usstocks": "https://xueqiu.com/v4/statuses/public_timeline_by_category.json?since_id=-1&count=10&category=101",
        "realestate": "https://xueqiu.com/v4/statuses/public_timeline_by_category.json?since_id=-1&count=10&category=111",
        "privatefund": "https://xueqiu.com/v4/statuses/public_timeline_by_category.json?since_id=-1&count=10&category=113",
        "cars": "https://xueqiu.com/v4/statuses/public_timeline_by_category.json?since_id=-1&count=10&category=114",
        "insurance": "https://xueqiu.com/v4/statuses/public_timeline_by_category.json?since_id=-1&&count=10&category=110"
    }

    endpoint = endpoints[category]

    next_max_id = -1

    ERROR_CODES = {
        "400016": "Unknown error."
    }

    while True:
        target = "{}&max_id={}".format(endpoint, next_max_id)
        print(target)
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
        }
        resp = requests.get(target, headers=headers)
        print(resp.text)
        break

if __name__ == "__main__":
    scrape("tech")






