#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from validator.name_validator import NameValidator


class TestNormalizeName(unittest.TestCase):

    def test_when_gets_empty_string_returns_(self):
        self.assertEqual('', NameValidator.normalize_name(name=''))

    def test_lowers_the_given_expression(self):
        self.assertEqual('bravosolution', NameValidator.normalize_name('BravoSolution'))

    def test_filters_whitespaces(self):
        self.assertEqual('commonsensemedia', NameValidator.normalize_name('Common Sense Media'))

    def test_filters_leading_and_trailing_whitespaces(self):
        self.assertEqual('infinityinsurancecompany',
                         NameValidator.normalize_name('       \tInfinity Insurance Company\t'))

    def test_filters_extensions_with_companyextensionfilter(self):
        self.assertEqual('smithmicrosoftware', NameValidator.normalize_name('Smith Micro Software, Inc.'))

    def filters_punctuation(self):
        self.assertEqual('libertymutualinsurancelibertymutualcom',
                         NameValidator.normalize_name('Liberty Mutual Insurance / libertymutual.com'))

if __name__ == '__main__':
    unittest.main(verbosity=2)