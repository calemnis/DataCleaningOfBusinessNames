#!/usr/local/bin python3
# -*- coding:utf-8 -*-

import unittest
from separator_logic import filter_redundant


class TestFilteringPortionLicense(unittest.TestCase):

    def test_filters_word_before_license(self):
        self.assertEqual('', filter_redundant('Sales License'))

    def test_filters_word_before_portion(self):
        self.assertEqual('', filter_redundant('Asia Portion'))

    def test_does_not_filter_when_no_expression(self):
        self.assertEqual('', filter_redundant(''))

    def test_does_not_filter_after_expression(self):
        self.assertEqual(' of Veolia Group UK', filter_redundant('Associate License of Veolia Group UK'))

    def test_filters_only_one_word_before_exprression(self):
        self.assertEqual('Zebra Technologies (APAC)', filter_redundant('Zebra Technologies (APAC Singapore Portion)'))

if __name__ == '__main__':
    unittest.main(verbosity=2)
