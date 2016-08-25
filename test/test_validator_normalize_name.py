#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from validator.name_validator import NameValidator
from cleaner.extension_cleaner import CompanyExtensionCleaner


class TestNormalizeName(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.extension_cleaner = CompanyExtensionCleaner('files/company_extensions.txt')

    # # TODO this wont work like this...
    # def test_when_gets_empty_string_returns_(self):
    #     self.assertEqual('', NameValidator.normalize_name(NameValidator, name=''))

if __name__ == '__main__':
    unittest.main(verbosity=2)