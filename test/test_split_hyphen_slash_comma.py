#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from separator_logic import split_by_delimiters


class TestHyphenCasesAsDelimiters(unittest.TestCase):

    def test_split_by_space_hyphen_space(self):
        self.assertEqual(["Recruit Lifestyle Co. Ltd.", "UX Design Group"],
                         split_by_delimiters("Recruit Lifestyle Co. Ltd. - UX Design Group"))

    def test_split_by_space_hyphen_word(self):
        self.assertEqual(["Brescia University ", "TimeZone"], split_by_delimiters("Brescia University -TimeZone"))

    def test_does_not_split_by_word_hyphen_space(self):
        self.assertTrue(["Hotel- og Restaurantskolen"], split_by_delimiters("Hotel- og Restaurantskolen"))

    def test_does_not_split_by_word_hyphen_word(self):
        self.assertEqual(["Can-Do Ideas"], split_by_delimiters("Can-Do Ideas"))


class TestSlashCasesAsDelimiters(unittest.TestCase):

    def test_split_by_space_slash_space(self):
        self.assertEqual(["Second Life", "Linden Lab"], split_by_delimiters("Second Life / Linden Lab"))

    def test_split_by_space_slash_word(self):
        self.assertEqual(["Welend ", "Wolaidai"], split_by_delimiters("Welend /Wolaidai"))

    def test_split_by_word_slash_space(self):
        self.assertTrue(["Study Group", "Taylors college"], split_by_delimiters("Study Group/ Taylors college"))

    def test_does_not_split_by_word_slash_word(self):
        self.assertEqual(["Kingo Karlsen A/S"], split_by_delimiters("Kingo Karlsen A/S"))
        self.assertEqual(["Miller/Howard Investments"], split_by_delimiters("Miller/Howard Investments"))


class TestCommaCasesAsDelimiters(unittest.TestCase):

    def test_split_by_space_comma_space(self):
        self.assertEqual(["Customers Bank", "BankMobile"], split_by_delimiters("Customers Bank , BankMobile"))

    def test_does_not_split_by_space_comma_word(self):
        self.assertEqual(["There Is No Business ,Name Like This"],
                         split_by_delimiters("There Is No Business ,Name Like This"))

    def test_does_not_split_by_word_comma_space(self):
        self.assertTrue(["Katitas Co, Ltd"], split_by_delimiters("Katitas Co, Ltd"))

    def test_split_by_word_comma_word(self):
        self.assertTrue(["OmniTRAX", "Port of Churchill"], split_by_delimiters("OmniTRAX,Port of Churchill"))

    def test_does_not_split_by_digit_comma_digit(self):
        self.assertEqual(["1,6 miljonerklubben"], split_by_delimiters("1,6 miljonerklubben"))

if __name__ == '__main__':
    unittest.main(verbosity=2)