#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from src.separator_logic import strip_elements


class TestStrip(unittest.TestCase):

    def test_cleans_string_with_redundant_tab_expression(self):
        self.assertEqual(["Estee Lauder"], strip_elements([r'Estee Lauder\t']))
        self.assertEqual(["Kumon Deutschland"], strip_elements([r"Kumon Deutschland   \t"]))


if __name__ == '__main__':
    unittest.main(verbosity=2)