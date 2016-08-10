#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from data_cleaner.cleaner.country_cleaner import CountriesCleaner


class TestCountriesCleaner(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.cleaner = CountriesCleaner('data_cleaner/files/countries_table.csv')

    def test_when_no_expression_returns_empty_string(self):
        self.assertEqual('', self.cleaner.filter_alone_countries(''))

    def test_when_alone_countries_filters(self):
        self.assertEqual('', self.cleaner.filter_alone_countries('France'))

    def test_two_worded_counties_filters(self):
        self.assertEqual('', self.cleaner.filter_alone_countries('United States'))

    def test_when_incorrect_form_of_country_name_does_not_filter(self):
        self.assertEqual('Saudi', self.cleaner.filter_alone_countries('Saudi'))

    def test_when_iso2_country_abbreviation_filters(self):
        self.assertEqual('', self.cleaner.filter_alone_countries('AU'))

    def test_when_iso3_country_abbreviation_filters(self):
        self.assertEqual('', self.cleaner.filter_alone_countries('AUS'))

    def test_when_alone_state_filters(self):
        self.assertEqual('', self.cleaner.filter_alone_countries('Arizona'))

    def test_when_two_worded_state_filters(self):
        self.assertEqual('', self.cleaner.filter_alone_countries('South Carolina'))

    def test_when_iso2_abbreviation_state_filters(self):
        self.assertEqual('', self.cleaner.filter_alone_countries('NY'))

    def test_when_country_not_alone_does_not_filter(self):
        self.assertEqual('Apacer HK', self.cleaner.filter_alone_countries('Apacer HK'))

    def test_when_country_name_not_english_does_not_filter(self):
        self.assertEqual('Ispanija', self.cleaner.filter_alone_countries('Ispanija'))

    def test_does_not_filter_regions(self):
        self.assertEqual('North Asia', self.cleaner.filter_alone_countries('North Asia'))


if __name__ == '__main__':
    unittest.main(verbosity=2)