#!/usr/local/bin python3
# -*- coding:utf-8 -*-

import unittest
from separator_logic import cut_redundant


class TestCuttingRedundantFormerlyExpressions(unittest.TestCase):

    def test_cuts_formerly_expression_alone(self):
        self.assertEqual('', cut_redundant('formerly'))

    def test_cuts_when_expression_in_parentheses(self):
        self.assertEqual('', cut_redundant('(formerly buy.com)'))

    def test_cuts_when_expression_in_parentheses_after_company(self):
        self.assertEqual('Community Health Systems ', cut_redundant('Community Health Systems (Formerly HMA)'))

    def test_cuts_when_expression_without_parentheses_after_company(self):
        self.assertEqual('Ergo Interactive', cut_redundant('Ergo Interactive Formerly know as Boombox INC'))

    def test_cuts_everything_after_formerly(self):
        self.assertEqual('American Gaming Systems ', cut_redundant('American Gaming Systems (Formerly Cadillac Jack / Amaya)'))

    def test_cuts_when_formerly_in_some_other_languages(self):
        self.assertEqual('IHS Global GmbH ', cut_redundant('IHS Global GmbH (ehemals iSuppli)'))

    def test_cuts_when_abbreviation_of_formerly_cases(self):
        self.assertEqual('Bank Australia ', cut_redundant('Bank Australia (former BankMecu)'))

if __name__ == '__main__':
    unittest.main(verbosity=2)
