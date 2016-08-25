#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
import os.path

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


class CompanyExtensionCleaner:

    def __init__(self, extensions_file):

        self.compiled_extensions = []
        with open(extensions_file, 'r') as extensions:
            for ext in extensions:
                self.compiled_extensions.append(ext.strip())

        self.compiled_extensions = [re.compile(r'\b' + re.escape(ext) + r'\b')
                                      for ext in self.compiled_extensions]

    def filter_extensions(self, item):
        for compiled in self.compiled_extensions:
            item = compiled.sub('', item)
        return item