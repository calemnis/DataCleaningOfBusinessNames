#!/usr/bin/env python3
# -*- coding: utf8 -*-

def is_special(char):
    return not char.isalnum() and not char.isspace()

if __name__ == '__main__':
    import unittest
    import string

    class TestCharFilter(unittest.TestCase):
        def test_letter_is_not_special(self):
            for c in string.ascii_letters:
                self.assertEqual(False, is_special(c))

        def test_number_is_not_special(self):
            for d in string.digits:
                self.assertEqual(False, is_special(d))

        def test_punctuation_is_special(self):
            for d in string.punctuation:
                self.assertEqual(True, is_special(d))

        def test_accent_is_not_special(self):
            for c in 'árvíztükörtűrőfúrógép':
                self.assertEqual(False, is_special(c))

    unittest.main(verbosity=2)
