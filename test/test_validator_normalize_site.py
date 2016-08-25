#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from validator.name_validator import NameValidator


class TestNormalizeSite(unittest.TestCase):

    def test_when_no_site_(self):
        self.assertEqual('', NameValidator.normalize_site(''))

    def test_when_domain_gets_http(self):
        self.assertEqual('http://neatco.com', NameValidator.normalize_site('neatco.com'))

    def test_when_contains_uppercase_characters_site_gets_lowered(self):
        self.assertEqual('http://appro.com', NameValidator.normalize_site('Appro.com'))

    def test_when_starts_with_www_gets_http(self):
        self.assertEqual('http://www.etundra.com', NameValidator.normalize_site('www.etundra.com'))

    def test_when_contains_slash_t_removes_it(self):
        self.assertEqual('http://www.agta.org', NameValidator.normalize_site(r'\thttp://www.agta.org'))

    def test_when_contains_whitespaces_removes_them(self):
        self.assertEqual('http://www.sonoform.se', NameValidator.normalize_site('      http://www.sonoform.se'))

    def test_when_not_ascii_chars_able_to_normalize(self):
        self.assertEqual('http://www.spårbilar.se', NameValidator.normalize_site('www.spårbilar.se'))


if __name__ == '__main__':
    unittest.main(verbosity=2)