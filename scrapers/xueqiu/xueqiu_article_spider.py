import scrapy
import pymongo
from bs4 import BeautifulSoup

class XueqiuArticleSpider(scrapy.Spider):
    name = "xueqiu_article_spider"
    download_delay = 1.5

    def __init__(self, link_collection=None, article_collection=None, **kwargs):
        if link_collection is None or article_collection is None:
            quit()

        print("[info] Using {} as MongoDB collection".format(link_collection))
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["bluefire"]
        self.link_col = self.db[link_collection]
        self.article_col = self.db[article_collection]
        super().__init__(**kwargs)
    
    def _format_link(self, url):
        if "xueqiu.com" not in url:
            return "https://xueqiu.com{}".format(url)
        return url

    def start_requests(self):
        urls = [
            (self._format_link(doc["link"]), doc["article_id"], doc["created_at"])
            for doc in list(self.link_col.find({}, projection={
                "link": 1,
                "article_id": 1,
                "created_at": 1
            }))
        ]

        for url, article_id, created_at in urls:
            yield scrapy.Request(url, callback=self.parse, headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
                "Cookie": "_ga=GA1.2.1831851797.1552318131; device_id=fdac4e98e251135f1d9358c29c86f6f5; s=fi11i3vu0x; xq_a_token=81d45773abb1b366e832845c99c1c70dc9657551; xq_a_token.sig=8GjDWaPUPffpVUZFEG1Qw4rtM-U; xq_r_token=b9b80f015be55a28a155ffd7b95102c453a7273f; xq_r_token.sig=Xcs0PISsRDxf4ZvBdguYPn4t2oU; u=791553533010243"
            }, meta={"url": url, "article_id": article_id, "created_at": created_at})

    def parse(self, response):
        url = response.meta["url"]
        article_id = response.meta["article_id"]
        created_at = response.meta["created_at"]
        content = response.css("article").get()
        content_stripped = BeautifulSoup(content).get_text()
        title = response.xpath("//title/text()").get()

        self.article_col.update_one(
            {"article_id": article_id},
            {"$set" : {
                "url": url,
                "article_id": article_id,
                "created_at": created_at,
                "content": content_stripped,
                "title": title
            }},
            upsert=True)
