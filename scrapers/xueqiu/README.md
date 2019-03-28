# Xueqiu (雪球) scrapers

## Dependencies/Requirements
* `pymongo` (and a running local instance of MongoDB)
* `scrapy`
* `beautifulsoup4`

## Running the scrapers
```
$ python xueqiu_link_scraper.py <category>
```

`<category>` can be any one of the following: 
  * `hkstocks` (港股)
  * `headlines` (头条)
  * `hushen` (沪深)
  * `insurance` (保险)
  * `livenews` (直播)
  * `privatefund` (私募)
  * `property` (房产)

This will save the **links to articles** to a collection called `xueqiu_<category>_links_<timestamp>` in the local instance of MongoDB, in a database called `bluefire` (this can be changed in the source).

```
$ scrapy runspider xueqiu_article_spider.py -a link_collection=<NAME OF COLLECTION WITH LINKS> -a article_collection=<NAME OF COLLECTION TO STORE THE ARTICLES>
```

This will run the scraper to retrieve the **content of the articles** using the links stored in the collection used by `xueqiu_link_scraper.py`. The second argument to the command is the name of the collection that the scraper should save the articles to. This can be arbitrary, but it will be used in the `xueqiu_comments_scraper.py` as well.

## Exporting the articles to JSON

The collection that stores the articles can be exported as JSON format using the `mongoexport` utility, as follows:

```
mongoexport --db "bluefire" --collection "COLLECTION_WITH_ARTICLES_NAME" --out "ARTICLES_OUTPUT_FILE_NAME.json"
```