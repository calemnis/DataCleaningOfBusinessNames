#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from separator_logic import split_by_delimiters


class TestBracketsAsDelimiters(unittest.TestCase):

    def test_splits_by_parenthesis_delimiter(self):
        self.assertEqual(['Alpargatas, Inc. ', 'havaianas.com', ''],
                         split_by_delimiters("Alpargatas, Inc. (havaianas.com)"))

    def test_splits_in_presence_of_two_parenthesis_pairs(self):
        self.assertEqual(['Wazee Digital Inc. ', 'T3Media', ' ',  'Thought Equity Motion', ''],
                         split_by_delimiters('Wazee Digital Inc. (T3Media) (Thought Equity Motion)'))

    def test_splits_when_parentheses_are_odd_numbered(self):
        self.assertEqual(["Parkinson's UK ", "Formerly The Parkinson's Disease Society ", "PDS", ''],
                         split_by_delimiters("Parkinson's UK (Formerly The Parkinson's Disease Society (PDS)"))

    def test_splits_when_parentheses_are_between_parentheses(self):
        self.assertEqual(["Marussia F1 ", "Virgin Racing ", "Manor Motorsport/GP", '', ''],
                         split_by_delimiters('Marussia F1 (Virgin Racing (Manor Motorsport/GP))'))

    def test_splits_when_more_than_one_parenthesis_pair_between_parentheses(self):
        self.assertEqual(["5 Udenrigsministeriet ", '', "Færøerne", " ", "lagmandskontoret", '', ''],
                         split_by_delimiters("5 Udenrigsministeriet ((Færøerne) (lagmandskontoret))"))

    def test_splits_by_box_brackets(self):
        self.assertEqual(["Mercury Public Affairs ", "Uganda", ''],
                         split_by_delimiters("Mercury Public Affairs [Uganda]"))

    def test_splits_in_presence_of_two_box_bracket_pairs(self):
        self.assertEqual(['', "6", " Alltel Corporation ", "Etc", ''],
                         split_by_delimiters("[6] Alltel Corporation [Etc]"))

    def test_split_handles_two_types_of_brackets(self):
        self.assertEqual(["Lenovo China ", "PC", ' ', "Do Not Reference", ''],
                         split_by_delimiters("Lenovo China (PC) [Do Not Reference]"))

    def test_splits_when_parentheses_between_box_brackets(self):
        self.assertEqual(["Wind River K.K. Global Deal_US ", "Asia ", "JP", " Portion", ""],
                         split_by_delimiters("Wind River K.K. Global Deal_US (Asia [JP] Portion)"))


if __name__ == '__main__':
    unittest.main(verbosity=2)
