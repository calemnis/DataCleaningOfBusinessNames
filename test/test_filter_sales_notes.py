#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from src.separator_logic import clean_sales_notes


class TestSalesNotesFilter(unittest.TestCase):

    def test_simple_whole_word_occurrence(self):
        self.assertEqual('', clean_sales_notes('DO NOT REFERENCE'))

if __name__ == '__main__':
    unittest.main(verbosity=2)