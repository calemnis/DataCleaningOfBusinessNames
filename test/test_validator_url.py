#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from validator.name_validator import NameValidator


class TestUrlValidator(unittest.TestCase):

    def test_when_no_urls_returns_false(self):
        self.assertEqual(False, NameValidator.is_valid(''))

    def test_when_url_not_valid_returns_false(self):
        self.assertEqual(False, NameValidator.is_valid('http://'))

    def test_when_url_does_not_start_with_http_returns_false(self):
        self.assertEqual(False, NameValidator.is_valid('www.atkins.com'))

    def test_url_does_not_accept_emails(self):
        self.assertEqual(False, NameValidator.is_valid('kari.loken@tafjordkonsern.no'))

    def test_when_url_valid_returns_true(self):
        self.assertEqual(True, NameValidator.is_valid('http://ikat.org'))

    def test_url_may_contain_www_if_starts_with_http(self):
        self.assertEqual(True, NameValidator.is_valid('http://www.crunch.com'))

    def test_accepts_more_complex_urls(self):
        self.assertEqual(True, NameValidator.is_valid('http://manormotorsport.mfbiz.com/#/contact/4514603489'))

if __name__ == '__main__':
    unittest.main(verbosity=2)