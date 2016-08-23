#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from separator_logic import filter_redundant


class TestCountryJunkCleaner(unittest.TestCase):

    def test_when_alone_two_chars_does_not_filter(self):
        self.assertEqual('CZ', filter_redundant('CZ'))

    def test_when_two_chars_separated_by_slash_filters(self):
        self.assertEqual('', filter_redundant('NV/SA'))

    def test_when_any_length_of_two_chars_separated_by_slash_filters(self):
        self.assertEqual('', filter_redundant('UK/CA/US/AU/SG/HK'))

    def test_when_contains_three_chars_filters_only_two_char_items(self):
        self.assertEqual('UAE/', filter_redundant('UAE/US/AU/SG'))

    def test_when_contains_non_two_char_expression_filters_only_two_char(self):
        self.assertEqual('/Asia', filter_redundant('CN/HK/Asia'))

    def test_when_comma_plus_space_filters(self):
        self.assertEqual('', filter_redundant('HK, SG, CN'))


if __name__ == '__main__':
    unittest.main(verbosity=2)