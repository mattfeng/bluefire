import scrapy
import pymongo
from bs4 import BeautifulSoup

class CNStockNewsSpider(scrapy.Spider):
    name = "cnstock_spider"
    download_delay = 1.5

    def start_requests(self):
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["bluefire"]
        col = db["cnstock_2019-03-26_19-01-08"]
        urls = [
            link["link"]
            for link in list(col.find({}, projection={"link": 1}))
        ]

        for url in urls:
            yield scrapy.Request(url, callback=self.parse, headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
                "Cookie": "_ga=GA1.2.1831851797.1552318131; device_id=fdac4e98e251135f1d9358c29c86f6f5; s=fi11i3vu0x; xq_a_token=81d45773abb1b366e832845c99c1c70dc9657551; xq_a_token.sig=8GjDWaPUPffpVUZFEG1Qw4rtM-U; xq_r_token=b9b80f015be55a28a155ffd7b95102c453a7273f; xq_r_token.sig=Xcs0PISsRDxf4ZvBdguYPn4t2oU; u=791553533010243"
            })

    def parse(self, response):
        article = response.css("div.content").get()
        soup = BeautifulSoup(article)
        title = response.xpath("//title/text()").get()

        yield {
            "title": title,
            "text": soup.get_text(),
            "link": response.url
        }
