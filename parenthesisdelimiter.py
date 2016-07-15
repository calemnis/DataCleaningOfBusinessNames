#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#TODO

#junk cases identification
#positive and negative test cases for the junk

#grep

import unittest
from parenthesisdelimitermain import split_by_delimiters

if __name__ == '__main__':

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


    class TestSingleCharactersAsDelimiters(unittest.TestCase):

        def test_splits_when_word_vertical_line_word(self):
            self.assertEqual(["f.u.n. netzwerk", "nordbayern gmbh"],
                             split_by_delimiters("f.u.n. netzwerk|nordbayern gmbh"))

        def test_split_by_space_vertical_line_space(self):
            self.assertEqual(["Sagaland", "Yuandao"],
                             split_by_delimiters("Sagaland | Yuandao"))

        def test_split_by_space_vertical_line_word(self):
            self.assertEqual(["There Is No Business", "Name Like This"],
                             split_by_delimiters("There Is No Business |Name Like This"))

        def test_split_by_word_vertical_line_space(self):
            self.assertTrue(["Zapak", " Bigflix"], split_by_delimiters("Zapak| Bigflix"))

        def test_split_by_emdash(self):
            self.assertEqual(["Help", "Hilfe zur Selbsthilfe"],
                             split_by_delimiters("Help – Hilfe zur Selbsthilfe"))

    class TestNTupleCharOcurrencesAsDelimiters(unittest.TestCase):

        def test_splits_when_word_double_hyphens_word(self):
            self.assertEqual(["Tap4fun", "CH/HK"], split_by_delimiters("Tap4fun--CH/HK"))

        def test_splits_when_space_double_hyphens_space(self):
            self.assertEqual(["Dell", "Alienware Corporation"], split_by_delimiters("Dell -- Alienware Corporation"))

        def test_splits_when_more_than_two_hyphens(self):
            self.assertEqual(["Tap4fun", "CH/HK"], split_by_delimiters("Tap4fun---CH/HK"))
            self.assertEqual(["Tap4fun", "CH/HK"], split_by_delimiters("Tap4fun-----CH/HK"))

        def test_splits_when_at_least_two_star_symbols(self):
            self.assertEqual(["Verizon Business", "Do Not reference"],
                             split_by_delimiters("Verizon Business **Do Not reference**"))

        def test_does_not_split_when_one_star_symbol(self):
            self.assertEqual(["Lux* Resort & Hotel"],
                             split_by_delimiters("Lux* Resort & Hotel"))

        def test_split_when_more_than_two_star_symbols(self):
            self.assertEqual(["Fred Butler Sweden AB", "Konfidentiellt"],
                             split_by_delimiters("Fred Butler Sweden AB ****Konfidentiellt**** "))

        #def test_splits_when_only_one_backslash(self):
         #   self.assertEqual(["Estee Lauder\t"], split_by_delimiters('Estee Lauder"\\"t'))

        def test_splits_when_two_backslashes(self):
            self.assertEqual(["TBWA", "Hakuhodo Inc."], split_by_delimiters(r"TBWA\\Hakuhodo Inc."))

        def test_splits_when_more_than_two_backslashes(self):
            self.assertEqual(["No Business Name", "Like This Yet"],
                             split_by_delimiters("No Business Name\\\\ Like This Yet"))

        def test_splits_when_two_slashes(self):
            self.assertEqual(["Per Capita AB", "Dental 24"], split_by_delimiters("Per Capita AB // Dental 24"))

        def test_does_not_split_when_slash_is_part_of_URL(self):
            self.assertEqual(["http://services.meltwaterbuzz.com/svr38"],
                             split_by_delimiters("http://services.meltwaterbuzz.com/svr38"))


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

    unittest.main(verbosity=2)