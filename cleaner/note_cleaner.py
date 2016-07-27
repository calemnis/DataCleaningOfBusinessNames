#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
import os.path

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


class NotesCleaner:

    def __init__(self, stop_phrases_file):

        self.compiled_stop_phrases = []
        with open(stop_phrases_file, 'r') as stop_phrases:
            for phrase in stop_phrases:
                self.compiled_stop_phrases.append(phrase.strip())

        self.compiled_stop_phrases = [re.compile(r'\b' + phrase + r'\b', flags=re.IGNORECASE)
                                      for phrase in self.compiled_stop_phrases]

    def filter_sales_notes(self, item):
        # TODO
        # write tests for this
        for compiled in self.compiled_stop_phrases:
            item = compiled.sub('', item)
        return item
