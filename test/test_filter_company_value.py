#!/usr/local/bin python3
# -*- coding:utf-8 -*-

import unittest
from separator_logic import filter_redundant


class TestFilteringCompanyValue(unittest.TestCase):

    def test_returns_empty_when_input_list_is_empty(self):
        self.assertEqual('', filter_redundant(''))

    def test_filters_company_value_that_stands_alone(self):
        self.assertEqual('', filter_redundant('6k'))

    def test_filters_decimal_values(self):
        self.assertEqual('', filter_redundant('4.8k'))

    def test_filters_values_case_insensitive(self):
        self.assertEqual('', filter_redundant('7K'))

    def test_filters_unlimited_large_values(self):
        self.assertEqual('', filter_redundant('200K'))
        self.assertEqual('', filter_redundant('1000k'))

    def test_does_not_filter_without_value_character(self):
        self.assertEqual('Century 21', filter_redundant('Century 21'))

    def test_filters_when_company_value_at_the_end_of_string(self):
        self.assertEqual('Internap ', filter_redundant('Internap 20K'))

    def test_filters_when_space_between_number_and_character(self):
        self.assertEqual('CA Technologies  ', filter_redundant('CA Technologies 90 k '))

    def test_does_not_filter_when_word_characters_around_value(self):
        self.assertEqual('Fitwize4Kids', filter_redundant('Fitwize4Kids'))

    def test_filters_when_no_word_characters_around_value(self):
        self.assertEqual(' Games', filter_redundant('2K Games'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
