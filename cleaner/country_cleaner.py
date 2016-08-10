#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
import os.path

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

class CountriesCleaner:

    def extend_list(self, item):
        new_list = item.split(',')
        for item in new_list:
            if item is not '':
                self.countries_list.append(item.strip())

    def __init__(self, countries_file):

        self.compiled_countries = []
        self.countries_list = []

        with open(countries_file, 'r') as countries:
            [self.extend_list(row.strip()) for row in countries]

        self.compiled_countries = [re.compile(r'^' + country + r'$') for country in self.countries_list]


    def filter_alone_countries(self, item):

        for compiled in self.compiled_countries:
            alone_search_obj = compiled.search(item)
            if alone_search_obj:
                item = compiled.sub('', item)

        return item