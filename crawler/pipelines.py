# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from src.crawler.items import WebsiteItem, AboutItem
from src.init.config import get_results_file

class CrawlerPipeline(object):

    def __init__(self):

        print('INITIALIZING PIPELINE')
        # with open(get_results_file(), 'rt') as results:
        #     for row in results:
        #         print(row)

    def process_item(self, item, spider):


        print("PROCESSING")
        if isinstance(item, WebsiteItem):
            print('INSTANCE OF WEBSITE')

            return item
        elif isinstance(item, AboutItem):
            print('INSTANCE OF ABOUT')
            return item
