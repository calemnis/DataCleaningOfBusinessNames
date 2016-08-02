#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
import os.path
from src.init import config

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

#TODO write tests for this

class CountriesCleaner:

    def extend_list(self, item):
        new_list = item.split(',')
        for item in new_list:
            self.countries_list.append(item.strip())

    def __init__(self, countries_file, states_file):

        self.compiled_countries = []
        self.countries_list = []

        with open(countries_file, 'r') as countries:
            [self.extend_list(country.strip()) for country in countries]

        with open(states_file, 'r') as states:
            [self.extend_list(state.strip()) for state in states]

        self.compiled_countries = [re.compile(r'^' + country + r'$') for country in self.countries_list]

    def filter_junk(item):
        junk_search_obj = config.countries_junk_pattern.search(item)
        if junk_search_obj:
            item = re.sub(re.escape(junk_search_obj.group(0)), r'', item)

        return item

    def filter_alone_countries(self, item):

        for compiled in self.compiled_countries:
            alone_search_obj = compiled.search(item)
            if alone_search_obj:
                item = compiled.sub('', item)

        return item