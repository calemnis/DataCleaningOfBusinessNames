#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#TODO

#junk cases identification
#positive and negative test cases for the junk

#grep

import unittest
from src.parenthesisdelimitermain import split_by_delimiters
from src.parenthesisdelimitermain import clean_from_spaces


class TestBracketsAsDelimiters(unittest.TestCase):

    def test_splits_by_parenthesis_delimiter(self):
        self.assertEqual(['Alpargatas, Inc.', 'havaianas.com'],
                         split_by_delimiters("Alpargatas, Inc. (havaianas.com)"))

    def test_splits_in_presence_of_two_parenthesis_pairs(self):
        self.assertEqual(['Wazee Digital Inc.', 'T3Media', 'Thought Equity Motion'],
                         split_by_delimiters('Wazee Digital Inc. (T3Media) (Thought Equity Motion)'))

    def test_splits_when_parentheses_are_odd_numbered(self):
        self.assertEqual(["Parkinson's UK", "Formerly The Parkinson's Disease Society", "PDS"],
                         split_by_delimiters("Parkinson's UK (Formerly The Parkinson's Disease Society (PDS)"))

    def test_splits_when_parentheses_are_between_parentheses(self):
        self.assertEqual(["Marussia F1", "Virgin Racing", "Manor Motorsport/GP"],
                         split_by_delimiters('Marussia F1 (Virgin Racing (Manor Motorsport/GP))'))

    def test_splits_when_more_than_one_parenthesis_pair_between_parentheses(self):
        self.assertEqual(["5 Udenrigsministeriet", "Færøerne", "lagmandskontoret"],
                         split_by_delimiters("5 Udenrigsministeriet ((Færøerne) (lagmandskontoret))"))

    def test_splits_by_box_brackets(self):
        self.assertEqual(["Mercury Public Affairs", "Uganda"],
                         split_by_delimiters("Mercury Public Affairs [Uganda]"))

    def test_splits_in_presence_of_two_box_bracket_pairs(self):
        self.assertEqual(["6", "Alltel Corporation", "CST"], split_by_delimiters("[6] Alltel Corporation [CST]"))

    def test_split_handles_two_types_of_brackets(self):
        self.assertEqual(["Lenovo China", "PC", "Do Not Reference"],
                         split_by_delimiters("Lenovo China (PC) [Do Not Reference]"))

    def test_splits_when_parentheses_between_box_brackets(self):
        self.assertEqual(["Wind River K.K. Global Deal_US", "Asia", "JP", "Portion"],
                         split_by_delimiters("Wind River K.K. Global Deal_US (Asia [JP] Portion)"))

    def test_cleans_string_with_redundant_tab_expression(self):
        self.assertEqual(["Estee Lauder"], clean_from_spaces(['Estee Lauder\t']))
        self.assertEqual(["Kumon Deutschland"], clean_from_spaces(["Kumon Deutschland   \t"]))


class TestHyphenCasesAsDelimiters(unittest.TestCase):

    def test_split_by_space_hyphen_space(self):
        self.assertEqual(["Recruit Lifestyle Co. Ltd.", "UX Design Group"],
                         split_by_delimiters("Recruit Lifestyle Co. Ltd. - UX Design Group"))

    def test_split_by_space_hyphen_word(self):
        self.assertEqual(["Brescia University", "CST"], split_by_delimiters("Brescia University -CST"))

    def test_does_not_split_by_word_hyphen_space(self):
        self.assertTrue(["Hotel- og Restaurantskolen"], split_by_delimiters("Hotel- og Restaurantskolen"))

    def test_does_not_split_by_word_hyphen_word(self):
        self.assertEqual(["Can-Do Ideas"], split_by_delimiters("Can-Do Ideas"))


class TestSlashCasesAsDelimiters(unittest.TestCase):

    def test_split_by_space_slash_space(self):
        self.assertEqual(["Second Life", "Linden Lab 15K"], split_by_delimiters("Second Life / Linden Lab 15K"))

    def test_split_by_space_slash_word(self):
        self.assertEqual(["Welend", "Wolaidai"], split_by_delimiters("Welend /Wolaidai"))

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