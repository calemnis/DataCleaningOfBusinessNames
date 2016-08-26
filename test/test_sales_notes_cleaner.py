#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from cleaner.note_cleaner import NotesCleaner


class TestSalesNotesFilter(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.cleaner = NotesCleaner('files/stop_phrases.txt')

    def test_when_no_expression_returns_empty_string(self):
        self.assertEqual('', self.cleaner.filter_sales_notes(''))

    def test_filters_simple_whole_word_occurrence(self):
        self.assertEqual('', self.cleaner.filter_sales_notes('DO NOT REFERENCE'))

    def test_filters_other_forms_of_same(self):
        self.assertEqual('', self.cleaner.filter_sales_notes("DON'T REFERENCE"))

    def test_filters_case_insensitive(self):
        self.assertEqual('', self.cleaner.filter_sales_notes('dO noT RefeRENce'))

    def test_filters_multiple_phrases_in_one_string(self):
        self.assertEqual(';', self.cleaner.filter_sales_notes('Non-Disclosure Agreement;Do Not Reference'))
        self.assertEqual(' ', self.cleaner.filter_sales_notes('DO NOT REFERENCE NDA'))

    def test_does_not_filter_company(self):
        self.assertEqual('Clearwater Paper Corp- ',
                         self.cleaner.filter_sales_notes('Clearwater Paper Corp- DO NOT REFERENCE'))

    def test_when_NDA_is_only_part_of_string_filters_whole_expression(self):
        self.assertEqual('', self.cleaner.filter_sales_notes('NDA SIGNED'))

    def test_does_not_filter_privacy_note(self):
        self.assertEqual('! PRIVACY!', self.cleaner.filter_sales_notes('DO NOT REFERENCE! PRIVACY!'))

    def test_does_not_filter_privacy_business_name(self):
        self.assertEqual('Privacy Commissioner NZ', self.cleaner.filter_sales_notes('Privacy Commissioner NZ'))

    def test_when_only_confidential_filters(self):
        self.assertEqual('Bayer Healtcare Diabetes AS ',
                         self.cleaner.filter_sales_notes('Bayer Healtcare Diabetes AS confidential'))

    def test_when_confidential_somethings_filters_whole_expression(self):
        # the priority of the elements in the stop phrases file MATTERS.
        self.assertEqual('', self.cleaner.filter_sales_notes('CONFIDENTIAL CLIENT'))

    def test_does_not_filter_same_expressions_in_foreign_languages(self):
        self.assertEqual('Konfidentiellt konto', self.cleaner.filter_sales_notes('Konfidentiellt konto'))

if __name__ == '__main__':
    unittest.main(verbosity=2)
