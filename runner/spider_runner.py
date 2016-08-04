#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os.path
from twisted.internet import reactor
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
from src.crawler.spiders.company_site_crawler import CompanySiteSpider
from scrapy.utils.project import get_project_settings

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


class SpiderRunner:

    def __init__(self, raw_data_file):

        self.raw_data_file = raw_data_file

    def run_spider(self):


        # this starts a Twisted reactor, configures the logging and sets the shutdown handlers.
        # CrawlerProcess is needed instead of CrawlerRunner because of manual handling of the crawler process
        runner = CrawlerProcess(get_project_settings())

        # instantiating the spider
        spider = CompanySiteSpider()

        # scrapy uses this to set default log settings.
        #configure_logging()

        # starts a given Crawlers crawl method.
        # When the crawling is finished returns a deferred. (késleltetés)
        d = runner.crawl(spider, websites_file=self.raw_data_file)

        # this is a callback, to manually stop the reactor after the crawling finished.
        # also works as an errback
        d.addBoth(lambda _: reactor.stop())

        # the script is blocked here until the crawling is finished.
        reactor.run()
