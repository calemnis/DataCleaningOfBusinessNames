#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from src.separator_logic import separate_elements


class TestHyphenCasesAsDelimiters(unittest.TestCase):

    def test_split_by_space_hyphen_space(self):
        self.assertEqual(["Recruit Lifestyle Co. Ltd.", "UX Design Group"],
                         separate_elements("Recruit Lifestyle Co. Ltd. - UX Design Group"))

    def test_split_by_space_hyphen_word(self):
        self.assertEqual(["Brescia University", "TimeZone"], separate_elements("Brescia University -TimeZone"))

    def test_does_not_split_by_word_hyphen_space(self):
        self.assertTrue(["Hotel- og Restaurantskolen"], separate_elements("Hotel- og Restaurantskolen"))

    def test_does_not_split_by_word_hyphen_word(self):
        self.assertEqual(["Can-Do Ideas"], separate_elements("Can-Do Ideas"))


class TestSlashCasesAsDelimiters(unittest.TestCase):

    def test_split_by_space_slash_space(self):
        self.assertEqual(["Second Life", "Linden Lab 15K"], separate_elements("Second Life / Linden Lab 15K"))

    def test_split_by_space_slash_word(self):
        self.assertEqual(["Welend", "Wolaidai"], separate_elements("Welend /Wolaidai"))

    def test_split_by_word_slash_space(self):
        self.assertTrue(["Study Group", "Taylors college"], separate_elements("Study Group/ Taylors college"))

    def test_does_not_split_by_word_slash_word(self):
        self.assertEqual(["Kingo Karlsen A/S"], separate_elements("Kingo Karlsen A/S"))
        self.assertEqual(["Miller/Howard Investments"], separate_elements("Miller/Howard Investments"))


class TestCommaCasesAsDelimiters(unittest.TestCase):

    def test_split_by_space_comma_space(self):
        self.assertEqual(["Customers Bank", "BankMobile"], separate_elements("Customers Bank , BankMobile"))

    def test_does_not_split_by_space_comma_word(self):
        self.assertEqual(["There Is No Business ,Name Like This"],
                         separate_elements("There Is No Business ,Name Like This"))

    def test_does_not_split_by_word_comma_space(self):
        self.assertTrue(["Katitas Co, Ltd"], separate_elements("Katitas Co, Ltd"))

    def test_split_by_word_comma_word(self):
        self.assertTrue(["OmniTRAX", "Port of Churchill"], separate_elements("OmniTRAX,Port of Churchill"))

    def test_does_not_split_by_digit_comma_digit(self):
        self.assertEqual(["1,6 miljonerklubben"], separate_elements("1,6 miljonerklubben"))

if __name__ == '__main__':
    unittest.main(verbosity=2)