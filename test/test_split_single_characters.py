#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from separator_logic import split_by_delimiters


class TestSingleCharactersAsDelimiters(unittest.TestCase):

    def test_splits_when_word_vertical_line_word(self):
        self.assertEqual(["f.u.n. netzwerk", "nordbayern gmbh"],
                         split_by_delimiters("f.u.n. netzwerk|nordbayern gmbh"))

    def test_split_by_space_vertical_line_space(self):
        self.assertEqual(["Sagaland ", " Yuandao"],
                         split_by_delimiters("Sagaland | Yuandao"))

    def test_split_by_space_vertical_line_word(self):
        self.assertEqual(["There Is No Business ", "Name Like This"],
                         split_by_delimiters("There Is No Business |Name Like This"))

    def test_split_by_word_vertical_line_space(self):
        self.assertTrue(["Zapak", " Bigflix"], split_by_delimiters("Zapak| Bigflix"))

    def test_split_by_emdash(self):
        self.assertEqual(["Help ", " Hilfe zur Selbsthilfe"],
                         split_by_delimiters("Help – Hilfe zur Selbsthilfe"))

if __name__ == '__main__':
    unittest.main(verbosity=2)