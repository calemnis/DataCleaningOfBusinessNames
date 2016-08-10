#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from data_cleaner.separator_logic import strip_elements


class TestStrip(unittest.TestCase):

    def test_cleans_string_with_redundant_tab_expression(self):
        self.assertEqual(["Estee Lauder"], strip_elements([r'Estee Lauder\t']))
        self.assertEqual(["Kumon Deutschland"], strip_elements([r"Kumon Deutschland   \t"]))

    def test_cleans_string_with_redundant_leading_spaces(self):
        self.assertEqual(["Leading Spaces Inc."], strip_elements([r'     Leading Spaces Inc.']))

    def test_cleans_string_with_trailing_spaces(self):
        self.assertEqual(["Trailing Spaces Inc."], strip_elements([r'Trailing Spaces Inc.    ']))

    def test_clears_nonetypes_from_string(self):
        self.assertEqual(['No NoneTypes'], strip_elements([r'No NoneTypes', '']))
        
if __name__ == '__main__':
    unittest.main(verbosity=2)