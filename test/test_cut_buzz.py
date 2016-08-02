#!/usr/local/bin python3
# -*- coding:utf-8 -*-

import unittest
from src.separator_logic import cut_redundant


class TestCuttingRedundantBuzz(unittest.TestCase):

    def test_cuts_http_buzz_expression_alone(self):
        self.assertEqual('', cut_redundant('http://services.meltwaterbuzz.com/svr64'))

    def test_filters_www_buzz_expression(self):
        self.assertEqual('', cut_redundant('www.meltwaterbuzz.com/svr35'))

    def test_filters_everything_after_http(self):
        self.assertEqual('', cut_redundant('http://services.meltwaterbuzz.com/svr24, username: asthnjh, password: mtj'))

    def test_does_not_filter_without_http(self):
        self.assertEqual('username: asthnjh, password: mtj', cut_redundant('username: asthnjh, password: mtj'))

    def test_does_not_filter_only_buzz_not_part_of_website_information(self):
        self.assertEqual('Buzz Concepts', cut_redundant('Buzz Concepts'))

    def test_filters_only_buzz_when_list_contains_company_name(self):
        self.assertEqual('Victorinox AG', cut_redundant('Victorinox AG http://services.meltwaterbuzz.com/svr73'))

    def test_filters_only_buzz_when_expression_before_http(self):
        self.assertEqual('server', cut_redundant('server:http://services.meltwaterbuzz.com/svr98'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
