#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#TODO

#junk cases identification
#positive and negative test cases for the junk

#grep

import unittest
from src.separator_logic import separate_elements
from src.separator_logic import strip_elements


class TestBracketsAsDelimiters(unittest.TestCase):

    def test_splits_by_parenthesis_delimiter(self):
        self.assertEqual(['Alpargatas, Inc.', 'havaianas.com'],
                         separate_elements("Alpargatas, Inc. (havaianas.com)"))

    def test_splits_in_presence_of_two_parenthesis_pairs(self):
        self.assertEqual(['Wazee Digital Inc.', 'T3Media', 'Thought Equity Motion'],
                         separate_elements('Wazee Digital Inc. (T3Media) (Thought Equity Motion)'))

    def test_splits_when_parentheses_are_odd_numbered(self):
        self.assertEqual(["Parkinson's UK", "Formerly The Parkinson's Disease Society", "PDS"],
                         separate_elements("Parkinson's UK (Formerly The Parkinson's Disease Society (PDS)"))

    def test_splits_when_parentheses_are_between_parentheses(self):
        self.assertEqual(["Marussia F1", "Virgin Racing", "Manor Motorsport/GP"],
                         separate_elements('Marussia F1 (Virgin Racing (Manor Motorsport/GP))'))

    def test_splits_when_more_than_one_parenthesis_pair_between_parentheses(self):
        self.assertEqual(["5 Udenrigsministeriet", "Færøerne", "lagmandskontoret"],
                         separate_elements("5 Udenrigsministeriet ((Færøerne) (lagmandskontoret))"))

    def test_splits_by_box_brackets(self):
        self.assertEqual(["Mercury Public Affairs", "Uganda"],
                         separate_elements("Mercury Public Affairs [Uganda]"))

    def test_splits_in_presence_of_two_box_bracket_pairs(self):
        self.assertEqual(["6", "Alltel Corporation", "Etc"], separate_elements("[6] Alltel Corporation [Etc]"))

    def test_split_handles_two_types_of_brackets(self):
        self.assertEqual(["Lenovo China", "PC", "Do Not Reference"],
                         separate_elements("Lenovo China (PC) [Do Not Reference]"))

    def test_splits_when_parentheses_between_box_brackets(self):
        self.assertEqual(["Wind River K.K. Global Deal_US", "Asia", "JP", "Portion"],
                         separate_elements("Wind River K.K. Global Deal_US (Asia [JP] Portion)"))


if __name__ == '__main__':
    unittest.main(verbosity=2)