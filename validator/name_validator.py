#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pymysql.cursors
import csv
import os
import sys
import re
import tldextract
import validators
import unicodedata
import string
import Levenshtein
from cleaner.extension_cleaner import CompanyExtensionCleaner
from validator.registration import Registration

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


class NameValidator:

    def __init__(self, cleaned_file):

        self.cleaned_file = cleaned_file
        self.connection = pymysql.connect(host='localhost', user='root', passwd='', db='orb_companies', charset='utf8',
                                          cursorclass=pymysql.cursors.DictCursor,
                                          autocommit=False)
        self.cursor = self.connection.cursor()
        self.extension_cleaner = CompanyExtensionCleaner('files/company_extensions.txt')
        self.cleaned_results = 'files/cleaned_results.csv'
        self.registrations = []

    @staticmethod
    def is_valid(url):
        if url:
            if validators.url(url):
                return True
        return False

    @staticmethod
    def get_ratio(first, second):
        return Levenshtein.ratio(first, second)

    @staticmethod
    def get_jaro(first, second):
        return Levenshtein.jaro(first, second)

    @staticmethod
    def normalize_name(name, extension_cleaner=CompanyExtensionCleaner('files/company_extensions.txt')):
        name = extension_cleaner.filter_extensions(name)
        name = name.lower()

        exclude = set(string.punctuation + string.whitespace)
        name = ''.join(ch for ch in name if ch not in exclude)

        byte_string = str.encode(name)
        unicode_string = byte_string.decode('utf-8')
        nfkd_form = unicodedata.normalize('NFKD', unicode_string)

        result = u''.join([n for n in nfkd_form if not unicodedata.combining(n)])
        return result

    @staticmethod
    def normalize_site(website):
        pattern = re.compile(r'\\t')
        search_obj = pattern.search(website)
        if search_obj:
            website = pattern.sub('', website)

        website = website.lower().strip()
        if website.startswith('www') or validators.domain(website):
            website = 'http://' + website
        return website

    @staticmethod
    def get_domain(website):
        extracted = tldextract.extract(website)
        domain = extracted.registered_domain
        return domain

    def find_by_webdomain(self, domain):

        result = self.cursor.execute('''
            SELECT orb_num, name, normalized, country
            FROM orb_companies.orb_companies_domains d INNER JOIN
                 orb_companies.normalized_companies c
                 USING(orb_num)
            WHERE d.webdomain=%s''', domain)
        return result

    @staticmethod
    def find_with_weight(examined_names, normalized, weight):
        ratio = 0
        for name in examined_names:
            ratio = NameValidator.get_ratio(name, normalized) + weight
            if ratio > 0.5:
                return ratio
        return ratio

    @staticmethod
    def find_with_jaro(examined_names, normalized):

        first_name = examined_names[0]
        ratio = NameValidator.get_jaro(first_name, normalized)
        if ratio > 0.60:
            return ratio
        return ratio

    def find_by_normalized(self, examined_names, account_name, account_country, account_id):

        found = False
        for name in examined_names:

            result = self.cursor.execute('''
                select orb_num, BINARY name, country from orb_companies.normalized_companies
                where normalized = %s  union
                select orb_num, BINARY alternative, '' as 'column 3' from orb_companies.normalized_names
                where normalized_alternative = %s''', (name, name))

            if result:
                record = self.cursor.fetchall()

                for r in record:
                    name = r['BINARY name'].decode('utf-8')
                    if r['country'] == account_country:
                        # gets a pseudo ratio of 0.99, because the website returned a result in the database
                        # and the country is the same
                        pseudo_ratio = 0.99
                    else:
                        pseudo_ratio = 0.6

                    reg = Registration(account_id, account_name, r['orb_num'], name, r['country'], pseudo_ratio)
                    self.registrations.append(reg)
                    found = True

        if not found:
            reg = Registration(account_id, account_name, '', '', '', 0.0)
            self.registrations.append(reg)

        return found

    @staticmethod
    def prepare_candidates(row):

        cleaned_names = row['cleaned_name']
        examined_names_list = cleaned_names.split('\t')
        normalized_original = NameValidator.normalize_name(row['name'])
        normalized_registry = NameValidator.normalize_name(row['company_registration_name'])

        if normalized_registry:
            examined_names_list.append(normalized_registry)
        examined_names_list.append(normalized_original)

        examined_names_list = [NameValidator.normalize_name(name) for name in examined_names_list]
        return examined_names_list

    @staticmethod
    def adjust_weight(normalized, country, row):

        cleaned_names = row['cleaned_name']
        account_country = row['country']
        examined_names_list = cleaned_names.split('\t')

        first_name = examined_names_list[0]

        weight = 0
        if first_name:
            first_name = first_name.split()[0]
            first_norm = NameValidator.normalize_name(first_name)
            if NameValidator.get_ratio(first_norm, normalized) == 1.0:
                weight += 0.20
        if account_country:
            if NameValidator.get_ratio(account_country, country) == 1.0:
                weight += 0.20

        return weight

    def get_result(self, normalized_website):
        domain = self.get_domain(normalized_website)
        result = self.find_by_webdomain(domain)
        return result

    def validate(self):

        with open(self.cleaned_file, 'rt') as candidates:
            reader = csv.DictReader(candidates)

            for row in reader:

                account_id = row['account_id']
                account_name = row['name']
                normalized_website = self.normalize_site(row['website'])
                examined_names = NameValidator.prepare_candidates(row)

                if NameValidator.is_valid(normalized_website) and self.get_result(normalized_website):

                    record = self.cursor.fetchone()
                    record_normalized = record['normalized']

                    weight = NameValidator.adjust_weight(record_normalized, record['country'], row)
                    levenshtein_ratio = self.find_with_weight(examined_names, record_normalized, weight)

                    if levenshtein_ratio > 0.5:
                        reg = Registration(account_id, account_name, record['orb_num'], record['name'],
                                           record['country'], levenshtein_ratio)
                        self.registrations.append(reg)

                    else:
                        jaro_ratio = self.find_with_jaro(examined_names, record_normalized)
                        if jaro_ratio > 0.6:
                            reg = Registration(account_id, account_name, record['orb_num'], record['name'],
                                               record['country'], jaro_ratio)
                            self.registrations.append(reg)
                        else:
                            reg = Registration(account_id, account_name, '', '', '', 0.0)
                            self.registrations.append(reg)

                elif self.find_by_normalized(examined_names, account_name, row['country'], account_id):
                    pass
                else:
                    reg = Registration(account_id, account_name, '', '', '', 0.0)
                    self.registrations.append(reg)

            self.write_to_file()

    def write_to_file(self):
        with open('files/all_results.csv', 'wt') as results:

            writer = csv.DictWriter(results,
                                    fieldnames=['account_id', 'account_name', 'name', 'ratio', 'orb_num', 'country'])
            writer.writeheader()

            for reg in self.registrations:

                writer.writerow({'account_id': reg['account_id'], 'account_name': reg['account_name'],
                                 'name': reg['name'], 'ratio': reg['ratio'], 'orb_num': reg['orb_num'],
                                 'country': reg['country']})
