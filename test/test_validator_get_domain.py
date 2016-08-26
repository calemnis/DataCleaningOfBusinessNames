#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from validator.name_validator import NameValidator


class TestGetDomain(unittest.TestCase):

    def test_when_no_website_returns_empty_string(self):
        self.assertEqual('', NameValidator.get_domain(''))

    def test_when_one_top_level_domain_gets_domain(self):
        self.assertEqual('phonera.se', NameValidator.get_domain('http://www.phonera.se'))

    def test_when_more_top_level_domains_gets_domain(self):
        self.assertEqual('napo.org.uk', NameValidator.get_domain('http://www.napo.org.uk/'))

    def test_when_subdomain_gets_domain(self):
        self.assertEqual('uni-wuerzburg.de', NameValidator.get_domain('http://www.presse.uni-wuerzburg.de/startseite/'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
