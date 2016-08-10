#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import scrapy
from data_cleaner.crawler.items import AboutItem, WebsiteItem, PageItem
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TCPTimedOutError, TimeoutError
import re

# TODO issues with request tcp timeout and etc.


def is_valid_url(url):
    if not url:
        return False

    regex = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url is not None and regex.search(url)

class CompanySiteSpider(scrapy.Spider):

    name = 'CompaniesSiteCrawler'

    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'result.json',
    }

    def __init__(self, websites_file=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.websites_file = websites_file
        print('***********')
        print(self.websites_file)

    def start_requests(self):

        with open(self.websites_file, 'r') as accounts:
            for row in accounts:
                file_array = row.split('\t')
                account_id = file_array[0]
                website_url = file_array[3].strip()
                if is_valid_url(website_url):
                    yield scrapy.Request(url=website_url,
                                         callback=self.parse, errback=self.handle_errors, meta={'url': account_id})

    def parse(self, response):
        print("------SCRAPING '%s'" % response.url)

        website_item = WebsiteItem()
        website_item['id'] = response.meta['url']
        website_item['url'] = response.url # response.url equals the site where the request was redirected
        yield website_item

        soup = BeautifulSoup(response.text, "xml")

        for a in soup.find_all("a", text=re.compile(r'About')):

            item = AboutItem()
            item['id'] = response.meta['url']

            item['url_title'] = a.string.strip()

            # <a>About</a>
            # a tag is used as an anchor/placeholder.
            try:
                relative = a['href']
            except KeyError:
                return

            base = response.url
            whole_link = urljoin(base, relative)
            item['about_url'] = whole_link
            yield item

    #         request = scrapy.Request(url=whole_link,
    #                                  callback=self.parse_about_page,
    #                                  errback=self.handle_errors, meta={'id': response.meta['url']})
    #         yield request
    #
    # def parse_about_page(self, response):
    #     soup = BeautifulSoup(response.text, 'html.parser')
    #     texts = soup.find_all(text=True)
    #
    #     def visible(element):
    #         if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
    #             return False
    #         elif re.match('<!--.*-->', str(element)):
    #             return False
    #         return True
    #
    #     item = PageItem()
    #     item['id'] = response.meta['id']
    #     text = filter(visible, texts)
    #     print(type(text))
    #     return
    #     item['content'] = text[0, 150]
    #     yield item


    # TODO problems arised here.
    def handle_errors(self, failure):
        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            #print('HttpError on ' + response.url)
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            #print('DNSLookupError on ' + request.url)
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            #print('TimeoutError on ' + request.url)
            self.logger.error('TimeoutError on %s', request.url)



