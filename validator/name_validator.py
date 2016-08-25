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

# TODO optimizing the validating function (code design)
# TODO check occurrences where normalized are the same, but original names are not
# TODO write tests for validator logic
# TODO write to a file, in a form that resembles this:
    # same id   name1   ratio
    # same id   name2   ratio
    # same id   name3   ratio

# count(*) for normalized_companies:
# countries number in normalized_companies: '29519043'
# states number in normalized_companies: '29519043'


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
        self.counter = 0

    # TODO test
    def is_valid(url):
        return validators.url(url)

    def get_ratio(self, first, second):
        return Levenshtein.ratio(first, second)

    def get_jaro(self, first, second):
        return Levenshtein.jaro(first, second)

    # TODO test
    def normalize_name(self, name):
        name = self.extension_cleaner.filter_extensions(name)
        name = name.lower()

        exclude = set(string.punctuation + string.whitespace)
        name = ''.join(ch for ch in name if ch not in exclude)

        byte_string = str.encode(name)
        unicode_string = byte_string.decode('utf-8')
        nfkd_form = unicodedata.normalize('NFKD', unicode_string)

        return u''.join([n for n in nfkd_form if not unicodedata.combining(n)])

    # TODO test
    def normalize_site(self, website):

        website = website.lower().strip()
        if website.startswith('www') or validators.domain(website):
            website = 'http://' + website

        regex = re.compile(r'\\t')
        website = regex.sub('', website)
        return website

    # TODO test
    def get_domain(self, website):
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

    def find_with_weight(self, examined_names, normalized, weight):

        ratio = 0
        try:

            for name in examined_names:
                ratio = self.get_ratio(name, normalized) + weight
                if ratio > 0.5:
                    return ratio
            return ratio

        except IndexError:
            print("AN INDEXERROR OCCURRED - WEIGHTING", examined_names)

    def find_with_jaro(self, examined_names, normalized):

        try:
            first_name = examined_names[0]
            ratio = self.get_jaro(first_name, normalized)
            if ratio > 0.60:
                return ratio
            return ratio
        except IndexError:
            print("AN INDEXERROR OCCURRED - JARO", examined_names)

    def find_by_normalized(self, examined_names, account_country, account_id):

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
                        reg = Registration(account_id, r['orb_num'], name, r['country'], ratio=0.99)
                        self.registrations.append(reg)
                        found = True
                    else:
                        reg = Registration(account_id, r['orb_num'], name, r['country'], ratio=0.6)
                        self.registrations.append(reg)

                self.counter += 1
        return found

    def prepare_candidates(self, row):

        cleaned_names = row['cleaned_name']
        examined_names_list = cleaned_names.split('\t')
        normalized_original = self.normalize_name(row['name'])
        normalized_registry = self.normalize_name(row['company_registration_name'])

        if normalized_registry:
            examined_names_list.append(normalized_registry)
        examined_names_list.append(normalized_original)

        examined_names_list = [self.normalize_name(name) for name in examined_names_list]
        return examined_names_list

    def adjust_weight(self, normalized, country, row):

        cleaned_names = row['cleaned_name']
        account_country = row['country']
        examined_names_list = cleaned_names.split('\t')

        first_name = examined_names_list[0]

        weight = 0
        if first_name and account_country:
            first_name = first_name.split()[0]
            first_norm = self.normalize_name(first_name)
            if self.get_ratio(first_norm, normalized) == 1.0:
                weight += 0.20
            if self.get_ratio(account_country, country) == 1.0:
                weight += 0.20
        return weight

    def validate(self):
        valid_result_success = 0
        valid_result_jaro = 0
        valid_result_failed = 0

        valid_no_result_success = 0
        valid_no_result_failed = 0

        no_valid_website_success = 0
        no_valid_website_failed = 0

        with open(self.cleaned_file, 'rt') as candidates:
            reader = csv.DictReader(candidates)

            for row in reader:

                website = row['website']
                account_country = row['country']
                account_id = row['account_id']
                normalized_website = self.normalize_site(website)
                examined_names = self.prepare_candidates(row)

                if normalized_website and NameValidator.is_valid(normalized_website):
                    domain = self.get_domain(normalized_website)

                    result = self.find_by_webdomain(domain)
                    if result:
                        record = self.cursor.fetchone()
                        normalized_record = record['normalized']
                        name = record['name']
                        country = record['country']
                        orb_num = record['orb_num']
                        weight = self.adjust_weight(normalized_record, country, row)

                        ratio = self.find_with_weight(examined_names, normalized_record, weight)

                        if ratio > 0.5:
                            reg = Registration(account_id, orb_num, name, country, ratio)
                            self.registrations.append(reg)
                            valid_result_success += 1

                        else:
                            ratio = self.find_with_jaro(examined_names, normalized_record)
                            if ratio > 0.6:
                                reg = Registration(account_id, orb_num, name, country, ratio)
                                self.registrations.append(reg)
                                valid_result_jaro += 1
                            else:
                                valid_result_failed += 1

                    elif self.find_by_normalized(examined_names, account_country, account_id):
                        valid_no_result_success += 1
                    else:
                        valid_no_result_failed += 1

                elif self.find_by_normalized(examined_names, account_country, account_id):
                    no_valid_website_success += 1
                else:
                    no_valid_website_failed += 1

            print("valid_result_success:", valid_result_success)
            print("valid_result_jaro:", valid_result_jaro)
            print("valid_result_failed:", valid_result_failed)

            print("valid_no_result_success:", valid_no_result_success)
            print("valid_no_result_failed:", valid_no_result_failed)

            print("no_valid_website_success", no_valid_website_success)
            print("no_valid_website_fail", no_valid_website_failed)

            print("counter", self.counter)
            print("REG_LENGTH:", len(self.registrations))

            self.write_to_file()

            # match: 70.53% of our websites exists in orb database - this is ~41813
            # 5647 not valid or there is not even a website, 53634 valid and from this 41813 exists in database

    def write_to_file(self):
        with open('files/all_results.csv', 'wt') as results:

            writer = csv.DictWriter(results, fieldnames=['account_id', 'name', 'ratio', 'orb_num', 'country'])
            writer.writeheader()

            for reg in self.registrations:

                writer.writerow({'account_id': reg['account_id'], 'name': reg['name'], 'ratio': reg['ratio'],
                                 'orb_num': reg['orb_num'], 'country': reg['country']})

    def load_csv(self):

        with open('files/account_paid_utf8.tsv', 'rt') as input_file:
            reader = csv.DictReader(input_file, delimiter='\t')
            with open('files/filtered_accounts_five.csv', 'wt') as results:
                writer = csv.DictWriter(results,
                                        fieldnames=['account_id', 'name', 'company_registration_name', 'website', 'country'])
                writer.writeheader()

                for row in reader:

                    writer.writerow({'account_id': row['account_id'], 'name': row['name'],
                                     'company_registration_name': row['company_registration_name'],
                                     'website': row['website'], 'country': row['country']})



