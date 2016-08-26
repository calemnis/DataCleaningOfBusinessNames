#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from cleaner.extension_cleaner import CompanyExtensionCleaner


class TestCompanyExtensionFilter(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.cleaner = CompanyExtensionCleaner(extensions_file='files/company_extensions.txt')

    def test_when_no_expression_returs_empty(self):
        self.assertEqual('', self.cleaner.filter_extensions(''))

    def test_filters_the_given_extensions(self):
        self.assertEqual('Furniture Made Easy ', self.cleaner.filter_extensions('Furniture Made Easy LLC'))

    def test_does_filter_punctuation_but_only_if_file_contains_expression_punctuated(self):
        self.assertEqual('Zipcar, .', self.cleaner.filter_extensions('Zipcar, Inc.'))

if __name__ == '__main__':
    unittest.main(verbosity=2)