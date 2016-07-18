#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from src.separator_logic import separate_elements


class TestSingleCharactersAsDelimiters(unittest.TestCase):

    def test_splits_when_word_vertical_line_word(self):
        self.assertEqual(["f.u.n. netzwerk", "nordbayern gmbh"],
                         separate_elements("f.u.n. netzwerk|nordbayern gmbh"))

    def test_split_by_space_vertical_line_space(self):
        self.assertEqual(["Sagaland", "Yuandao"],
                         separate_elements("Sagaland | Yuandao"))

    def test_split_by_space_vertical_line_word(self):
        self.assertEqual(["There Is No Business", "Name Like This"],
                         separate_elements("There Is No Business |Name Like This"))

    def test_split_by_word_vertical_line_space(self):
        self.assertTrue(["Zapak", " Bigflix"], separate_elements("Zapak| Bigflix"))

    def test_split_by_emdash(self):
        self.assertEqual(["Help", "Hilfe zur Selbsthilfe"],
                         separate_elements("Help – Hilfe zur Selbsthilfe"))

if __name__ == '__main__':
    unittest.main(verbosity=2)