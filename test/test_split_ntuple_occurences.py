#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from src.separator_logic import split_by_delimiters


class TestNTupleCharOcurrencesAsDelimiters(unittest.TestCase):

    def test_splits_when_word_double_hyphens_word(self):
        self.assertEqual(["Tap4fun", "CH/HK"], split_by_delimiters("Tap4fun--CH/HK"))

    def test_splits_when_space_double_hyphens_space(self):
        self.assertEqual(["Dell ", " Alienware Corporation"], split_by_delimiters("Dell -- Alienware Corporation"))

    def test_splits_when_more_than_two_hyphens(self):
        self.assertEqual(["Tap4fun", "CH/HK"], split_by_delimiters("Tap4fun---CH/HK"))
        self.assertEqual(["Tap4fun", "CH/HK"], split_by_delimiters("Tap4fun-----CH/HK"))

    def test_splits_when_at_least_two_star_symbols(self):
        self.assertEqual(["Verizon Business ", "Do Not reference", ""],
                         split_by_delimiters("Verizon Business **Do Not reference**"))

    def test_does_not_split_when_one_star_symbol(self):
        self.assertEqual(["Lux* Resort & Hotel"],
                         split_by_delimiters("Lux* Resort & Hotel"))

    def test_split_when_more_than_two_star_symbols(self):
        self.assertEqual(["Fred Butler Sweden AB ", "Konfidentiellt", " "],
                         split_by_delimiters("Fred Butler Sweden AB ****Konfidentiellt**** "))

    def test_splits_when_two_backslashes(self):
        self.assertEqual(["TBWA", "Hakuhodo Inc."], split_by_delimiters(r"TBWA\\Hakuhodo Inc."))

    def test_splits_when_more_than_two_backslashes(self):
        self.assertEqual(["No Business Name", " Like This Yet"],
                         split_by_delimiters("No Business Name\\\\ Like This Yet"))

    def test_splits_when_two_slashes(self):
        self.assertEqual(["Per Capita AB ", " Dental 24"], split_by_delimiters("Per Capita AB // Dental 24"))

    def test_does_not_split_when_slash_is_part_of_URL(self):
        self.assertEqual(["http://services.meltwaterbuzz.com/svr38"],
                         split_by_delimiters("http://services.meltwaterbuzz.com/svr38"))

if __name__ == '__main__':
    unittest.main(verbosity=2)