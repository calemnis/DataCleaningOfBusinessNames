# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from data_cleaner.config import get_results_file
from data_cleaner.crawler.items import PageItem
import csv

class CrawlerPipeline(object):

    def __init__(self):

        print('INITIALIZING PIPELINE')
        self.unique_ids = set()
        self.candidates = None

    def process_item(self, item, spider):

        if isinstance(item, PageItem):
            return

        self.unique_ids.add(item['id'])
        candidates_list = self.get_candidates(account_id=item['id'])
        print('CANDIDATES')
        print(candidates_list)
        print(len(self.unique_ids))

        return item

    def get_candidates(self, account_id):

        self.candidates = set()

        with open(get_results_file(), 'rt') as results:
            self.reader = csv.DictReader(results)
            for row in self.reader:
                if row['account_id'] == account_id:
                    if row['company_registration_name']:
                        self.candidates.add(row['company_registration_name'])
                    line = row['cleaned_name'].split('\t')
                    self.candidates.update(line)
                    break

        return self.candidates



        # print("PROCESSING")
        # if isinstance(item, WebsiteItem):
        #     print('INSTANCE OF WEBSITE')
        #
        #     return item
        # elif isinstance(item, AboutItem):
        #     print('INSTANCE OF ABOUT')
        #     return item
