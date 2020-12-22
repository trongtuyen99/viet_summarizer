# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlNewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class SohaItem(scrapy.Item):
    news_id = scrapy.Field()
    topic = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()


class Item24h(scrapy.Item):
    news_id = scrapy.Field()
    topic = scrapy.Field()
    title = scrapy.Field()
    sapo = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()
    # text = scrapy.Field()

