import scrapy
from crawl_news.items import SohaItem
from scrapy import Request
import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class CrawlAll(scrapy.Spider):
    # crawled_site = set()
    # queue_site = set()
    root_site = "https://soha.vn/"
    name = "soha_crawler"
    # link_pattern1 = "href=\"\/([\w\d-]*.htm)"
    # link_pattern = "data-popup-url=\"\/([\w\d-]*.htm)"
    with open('all_links.txt', 'r') as reader:
        start_urls = reader.read().split("\n")
    allowed_domains = 'soha.vn'

    # rules = (Rule(LinkExtractor(allow=[r'data-popup-url=\"\/([\w\d-]*.htm)']), callback='parse', follow=True), )

    def parse(self, response, **kwargs):
        # self.crawled_site.add(response.url)
        # with open('site_crawled', 'a') as writer:
        #     data = response.url + "\n"
        #     writer.write(data)
        # body = str(response.body)
        # links = re.findall(self.link_pattern, body)
        # for link in links:
        #     if link not in self.start_urls and link[-21:-4] > '20200901':
        #         ls = link
        #         if not ls.startswith('https://soha.vn'):
        #             ls = response.url + link
        #         self.queue_site.add(ls)
        news_id = response.url[-21:-4]
        topic_all = response.xpath('//*[@id="sohaSubCategories"]/a').get()
        try:
            topic = re.findall(r">(.*)<", topic_all)[0].strip()
        except:
            topic = response.url  # bug raise
        title = response.xpath('//*[@id="admWrapsite"]/div[3]/div/div[6]/div[2]/div[1]/main/article/header/h1/text()') \
            .get()

        description = response.xpath(
            '//*[@id="admWrapsite"]/div[3]/div/div[6]/div[2]/div[1]/main/article/div[1]/div[1]/h2/text()').getall()
        if description:
            description = description[-1].strip()
        else:
            description = "unknown"

        content_all = response.xpath('//*[@id="admWrapsite"]/div[3]/div/div[6]/div[2]/div[1]'
                                     '/main/article/div[1]/div[1]/div[4]/p').getall()
        content = ""
        for c in content_all:
            try:
                content += " " + re.findall("<p>(.*)</p>", c)[0].strip()
            except:
                pass
        item = SohaItem()
        item['news_id'] = news_id
        item['topic'] = topic
        item['title'] = title.strip()
        item['description'] = description
        item['content'] = content
        item['url'] = response.url
        return item
