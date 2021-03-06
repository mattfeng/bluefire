import scrapy
import json
import pymongo

class XueqiuCommentsSpider(scrapy.Spider):
    name = "xueqiu_comments_spider"

    def __init__(self, link_collection=None, article_collection=None, **kwargs):
        """
        link_collection: The name of the collection that stores the links to scrape.
        article_collection: The name of the collection that stores the articles that have been scraped.
        """

        if link_collection is None or article_collection is None:
            quit()

        print("[info] Using `{}` as MongoDB source (link) collection".format(link_collection))
        print("[info] Saving comments to Mongo collection `{}`".format(article_collection))

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
        # Weirdly, the article id that is returned by the API
        # isn't always the same as the article id at the end
        # of the URL; the one at the end of the URL is more
        # reliable (and is the one used in the comments API to
        # retrieve the comments for an article). Thus, we use
        # the article ID for identifying the right document in
        # our database collection, but not for retrieving comments.
        target = "https://xueqiu.com/statuses/comments.json?id={}&count=20&page=1&reply=false&asc=false&type=status&split=true"

        urls = [
            (self._format_link(doc["link"]), doc["article_id"], doc["created_at"])
            for doc in list(self.link_col.find({}, projection={
                "link": 1,
                "article_id": 1,
            }))
        ]

        for link, article_id, created_at in urls:
            yield scrapy.Request(link, callback=self.parse, headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
                "Cookie": "_ga=GA1.2.1831851797.1552318131; device_id=fdac4e98e251135f1d9358c29c86f6f5; s=fi11i3vu0x; xq_a_token=81d45773abb1b366e832845c99c1c70dc9657551; xq_a_token.sig=8GjDWaPUPffpVUZFEG1Qw4rtM-U; xq_r_token=b9b80f015be55a28a155ffd7b95102c453a7273f; xq_r_token.sig=Xcs0PISsRDxf4ZvBdguYPn4t2oU; u=791553533010243"
            }, meta={"link": link, "article_id": article_id, "created_at": created_at})

    def parse(self, response):
        link = response.meta["link"]
        article_id = response.meta["article_id"]
        created_at = response.meta["created_at"]
        content = response.css("article").get()
        content_stripped = BeautifulSoup(content).get_text()
        title = response.xpath("//title/text()").get()

        self.article_col.update_one(
            {"article_id": article_id},
            {"$set" : {
                "link": link,
                "article_id": article_id,
                "created_at": created_at,
                "content": content_stripped,
                "title": title
            }},
            upsert=True)
