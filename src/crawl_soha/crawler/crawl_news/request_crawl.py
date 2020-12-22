import requests
from lxml import html
import os
import re
import csv
crawled_url = set()
import csv
save_file = "soha_all.csv"
root_site = "https://soha.vn/"
if not os.path.isfile(save_file):
    with open(save_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["news_id", "toppic", "title", "description"])

with open('./spiders/init_site', 'r') as reader:
    start_urls = reader.read().split("\n")
i = 0
while i < 20:
    i += 1
    curl = start_urls.pop()
    print(curl)
    news_id = curl[-21:-4]
    crawled_url.add(curl)
    response = requests.get(curl)
    source = html.fromstring(response.content)

    topic = curl
    try:
        topic = source.xpath('//*[@id="sohaSubCategories"]/a[1]/text()')[0]
    except:
        pass
    try:

        title = source.xpath('//*[@id="admWrapsite"]/div[3]/div/div[6]/div[2]/div[1]/main/article/header/h1/text()')[0].\
                    replace("\r\n", '').strip()
    except:
        title = curl
    try:
        description = source.xpath('//*[@id="admWrapsite"]/div[3]/div/div[6]/div[2]/div[1]/\
                    main/article/div[1]/div[1]/h2/text()')[-1].replace("\r\n", '').strip()
    except:
        description = curl

    content_all = source.xpath('//*[@id="admWrapsite"]/div[3]/div/div[6]/div[2]/div[1]'
                                 '/main/article/div[1]/div[1]/div[4]/p')
    content = ""
    for c in content_all:
        docs = c.xpath('./text()')
        if not docs:
            docs = c.xpath('./span/text()')
        if docs:
            content += docs[0]

    # with open(save_file, 'a', newline='') as file:
    #     writer = csv.writer(file)
    #     writer.writerow([news_id, topic, title, description])

    links = re.findall(r"data-popup-url=\"\/([\w\d-]*.htm)", str(response.content))
    links = set(links)
    for link in links:
        full_link = link
        if not link.startswith('https:/'):
            full_link = root_site + link
        if full_link not in crawled_url and full_link[-21:-4] > '20200901':
            start_urls.insert(0, full_link)