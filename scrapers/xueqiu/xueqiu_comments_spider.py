import scrapy
import json
import pymongo

class XueqiuCommentsSpider(scrapy.Spider):
    name = "xueqiu_comments_spider"

    def __init__(self, link_collection=None, article_collection=None):
        """
        link_collection: The name of the collection that stores the links to scrape.
        article_collection: The name of the collection that stores the articles that have been scraped.
        """
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["bluefire"]
        self.link_col = self.db[self.link_collection]
        self.article_col = self.db[self.article_collection]

        urls = [
            "https://xueqiu.com{}".format(link["link"])
            for link in list(self.link_col.find({}, projection={"link": 1}))
        ]
