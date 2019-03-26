import scrapy
from bs4 import BeautifulSoup

class CNGlobalStock(scrapy.Spider):
    # modeled after: https://wallstreetcn.com/articles/3499602
    name = "wallstreetcn"
    start_urls = ["https://wallstreetcn.com/articles/3499602"]

    def parse(self, response):
        article_body = response.css("div.rich-text").get()
        soup = BeautifulSoup(article_body)

        yield {
            "title": response.xpath("//title/text()").get(),
            "text": soup.get_text(),
            "time": response.css("time::attr('datetime')").get()
        }

        next_page = response.css("div.nav-item.next a::attr('href')").get()

        # Follow the next page if one is found
        if next_page is not None:
            yield response.follow(next_page, self.parse)
