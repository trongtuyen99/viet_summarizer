import scrapy
from crawl_news.items import Item24h
from scrapy import Request
import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class CrawlAll(scrapy.Spider):
    name = "crawler_24h"
    
    link_pattern = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    

    with open('new_link.txt', 'r') as reader:
        start_urls = reader.read().split("\n")

    start_urls = list(set(start_urls))
    with open('crawled_link.txt', 'r') as reader:
        crawled_urls = reader.read().split("\n")

    crawled_urls = set(crawled_urls).union(set(start_urls))
    list_crawled_urls = list(crawled_urls)

    with open('crawled_link.txt', 'w') as writer:
        writer.write("\n".join(list_crawled_urls))
    
    with open('new_link.txt', 'w') as writer:
        writer.write("")  # clear file
    
    allowed_domains = "https://www.24h.com.vn"

    def parse(self, response, **kwargs):
        text = response.text
        inside_link = re.findall(self.link_pattern, text)
        print("lenght of inside link: ", len(inside_link))
        set_inside_link = []
        for link in inside_link:
          if link.startswith("https://www.24h.com.vn/") and link not in self.crawled_urls:
            set_inside_link.append(link)
        with open('new_link.txt', 'a') as writer:
          for link in set_inside_link:
            writer.write(link+"\n")


        news_id = response.url[-17:-5]  # check link bai viet phai co id
        try:
            topic = response.xpath('//*[@id="left"]/main/div/header/div/nav[1]/div[2]/ul/li/a/span/text()').get()
        except:
            topic = "missing"

        try:
            title = response.xpath('//*[@id="article_title"]/text()').get()
        except:
            title = "missing"

        try:
            sapo = response.xpath('//*[@id="article_sapo"]/text()').get()
        except:
            sapo = "missing"
        try:
            content = ""
            for i in range(1, 20):
                try:
                    content_all = response.xpath(f'//*[@id="article_body"]/p[{i}]/text()').get()
                    content += content_all
                except:
                    if "<img class=" in response.xpath(f'//*[@id="article_body"]/p[{i}]').get():
                        pass
                    else:
                        break
        except:
            content = "missing"
        item = Item24h()
        item['news_id'] = news_id
        item['topic'] = topic
        item['title'] = title
        item['sapo'] = sapo
        item['content'] = content
        item['url'] = response.url
        # item['text'] = response.text
        return item
