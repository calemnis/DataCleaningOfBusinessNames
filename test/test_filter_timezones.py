#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from separator_logic import filter_redundant


class TestFilteringTimezones(unittest.TestCase):

    def test_returns_empty_string_when_input_list_empty(self):
        self.assertEqual('', filter_redundant(''))

    def test_filters_when_timezone_stands_alone(self):
        self.assertEqual('', filter_redundant('EST'))
        self.assertEqual('', filter_redundant('PST'))

    def test_filters_when_timezone_is_at_the_end_of_string(self):
        self.assertEqual('DLA Piper', filter_redundant('DLA Piper PST'))

    def test_filters_when_timezone_is_in_middle_of_string(self):
        self.assertEqual('Kirtas Technologies, Inc- NY', filter_redundant('Kirtas Technologies, Inc- EST NY'))

    def test_does_not_filter_when_string_starts_with_timezone(self):
        self.assertEqual('PST Langara College', filter_redundant('PST Langara College'))

    def test_filters_when_timezone_is_separated_by_delimiter(self):
        self.assertEqual('Quicksilver Resources', filter_redundant('Quicksilver Resources-CST'))

    def test_does_not_filter_when_timezone_expression_has_word_character_before(self):
        self.assertEqual('UB C TEST', filter_redundant('UB C TEST'))

    def test_does_not_filter_when_two_timezones(self):
        self.assertEqual('Why two timezones? PST', filter_redundant('Why EST two timezones? PST'))

if __name__ == '__main__':
    unittest.main(verbosity=2)