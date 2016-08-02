import scrapy
from scrapy.spiders import CrawlSpider
from src.crawler.items import AboutItem
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re


def is_valid_url(url):
    regex = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url is not None and regex.search(url)


class CompanySiteSpider(CrawlSpider):

    name = 'SimpleCrawler'

    def __init__(self, websites_file=None, cleaned_file=None, *args, **kwargs):
        super(CompanySiteSpider, self).__init__(*args, **kwargs)
        self.cleaned_file = cleaned_file
        self.websites_file = websites_file
        print('***********')
        print(self.websites_file)

    def start_requests(self):

        urls_dict = {}

        with open(self.websites_file, 'r') as accounts:
            for row in accounts:
                file_array = row.split('\t')
                if file_array[3]:
                    urls_dict[file_array[0]] = file_array[3].strip()

        for key, url in urls_dict.items():
            if is_valid_url(url):
                yield scrapy.Request(url=url)
    #
    # def parse(self, response):
    #
    #     print("------SCRAPING '%s'" % response.url)
    #     soup = BeautifulSoup(response.text, "lxml")
    #     item = AboutItem()
    #
    #     for a in soup.find_all("a", text=re.compile(r'About')):
    #         item['title'] = a.string
    #         item['link'] = a['href']
    #         yield item


    def parse(self, response):
        print("------SCRAPING '%s'" % response.url)
        soup = BeautifulSoup(response.text, "lxml")
        item = AboutItem()

        for a in soup.find_all("a", text=re.compile(r'About')):
            item['title'] = a.string.strip()
            relative = a['href']
            base = response.url

            item['link'] = urljoin(base, relative)
            yield item




