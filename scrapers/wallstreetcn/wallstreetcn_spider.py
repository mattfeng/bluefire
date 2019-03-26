import scrapy
import json
import urllib
from bs4 import BeautifulSoup

class WallStreetCNSpider(scrapy.Spider):
    name = "WallStreetCN_Spider"

    base_url = "https://api.wallstreetcn.com/apiv1/content/fabricate-articles?channel=global&accept=article&limit=20"
    start_urls = [base_url]
    download_delay = 1.5

    custom_settings = {
        "DEPTH_PRIORITY": 1,
        "SCHEDULER_DISK_QUEUE": "scrapy.squeues.PickleFifoDiskQueue",
        "SCHEDULER_MEMORY_QUEUE": "scrapy.squeues.FifoMemoryQueue"
    }
    
    def parse(self, response):
        base_url = "https://api.wallstreetcn.com/apiv1/content/fabricate-articles?channel=global&accept=article&limit=20"

        data = json.loads(response.body).get("data", {})

        article_urls = []

        for item in data.get("items", []):
            if item["resource"]["is_priced"]:
                continue
            article_urls.append(item["resource"]["uri"])

        print("[i] fetching {} articles...".format(len(article_urls)))
        for url in article_urls:
            yield scrapy.Request(url, callback=self.parse_article)
        
        next_cursor = data.get("next_cursor", None)
        if next_cursor is not None:
            next_api_call = base_url + "&cursor=" + urllib.parse.quote_plus(next_cursor)
            print("[i] next api call: " + next_api_call)

            yield scrapy.Request(next_api_call, callback=self.parse)
    
    def parse_article(self, response):
        article_body = response.css("div.rich-text").get()
        soup = BeautifulSoup(article_body)

        print("[i] retrieved: " + response.url)

        yield {
            "title": response.xpath("//title/text()").get(),
            "text": soup.get_text(),
            "time": response.css("time::attr('datetime')").get()
        }

