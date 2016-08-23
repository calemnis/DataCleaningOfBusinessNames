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

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# TODO optimizing the validating function
# TODO orb_companies_names port to table and foreign key orb_num


class NameValidator:

    def __init__(self, cleaned_file):

        self.cleaned_file = cleaned_file
        self.connection = pymysql.connect(host='localhost', user='root', passwd='', db='orb_companies', charset='utf8',
                                          cursorclass=pymysql.cursors.DictCursor,
                                          autocommit=False)
        self.cursor = self.connection.cursor()
        self.extension_cleaner = CompanyExtensionCleaner('files/company_extensions.txt')
        self.cleaned_results = 'files/cleaned_results.csv'

    def is_valid(url):
        return validators.url(url)

    def get_ratio(self, first, second):
        return Levenshtein.ratio(first, second)

    def get_jaro(self, first, second):
        return Levenshtein.jaro(first, second)

    def normalize_name(self, name):
        name = self.extension_cleaner.filter_extensions(name)
        name = name.lower()

        exclude = set(string.punctuation + string.whitespace)
        name = ''.join(ch for ch in name if ch not in exclude)

        byte_string = str.encode(name)
        unicode_string = byte_string.decode('utf-8')
        nfkd_form = unicodedata.normalize('NFKD', unicode_string)

        return u''.join([n for n in nfkd_form if not unicodedata.combining(n)])

    def normalize_site(self, website):

        website = website.lower().strip()
        if website.startswith('www') or validators.domain(website):
            website = 'http://' + website

        regex = re.compile(r'\\t')
        website = regex.sub('', website)
        return website

    def get_domain(self, website):
        extracted = tldextract.extract(website)
        domain = extracted.registered_domain
        return domain

    def find_with_jaro(self, examined_names, normalized):

        try:
            first_name = examined_names[0]
            first_norm = self.normalize_name(first_name)
            if self.get_jaro(first_norm, normalized) > 0.60:
                return True
            return False
        except IndexError:
            print("AN INDEXERROR OCCURRED - JARO", examined_names)

    def find_by_normalized(self, examined_names):

        for name in examined_names:
            normalized_name = self.normalize_name(name)

            result = self.cursor.execute("SELECT name, normalized FROM orb_companies.normalized_companies WHERE normalized=%s",
                 normalized_name)

            if result:
                return True
        return False

    def find_with_weight(self, examined_names, normalized):

        try:
            weight = 0
            first_name = examined_names[0].split()[0]
            first_norm = self.normalize_name(first_name)
            if self.get_ratio(first_norm, normalized) == 1.0:
                weight = 0.20

            for examined_name in examined_names:
                normalized_name = self.normalize_name(examined_name)

                ratio = self.get_ratio(normalized_name, normalized) + weight
                if ratio > 0.50:
                    return True
            return False

        except IndexError:
            print("AN INDEXERROR OCCURRED - WEIGHTING", examined_names)

    def prepare_candidates(self, row):

        cleaned_names = row['cleaned_name']
        examined_names_list = cleaned_names.split('\t')
        normalized_original = self.normalize_name(row['name'])
        normalized_registry = self.normalize_name(row['company_registration_name'])

        if normalized_registry:
            examined_names_list.append(normalized_registry)
        examined_names_list.append(normalized_original)
        return examined_names_list

    def get_url_correspondence(self):
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
                normalized_website = self.normalize_site(website)
                examined_names = self.prepare_candidates(row)

                if normalized_website and NameValidator.is_valid(normalized_website):
                    domain = self.get_domain(normalized_website)

                    result = self.cursor.execute('''
                        SELECT name, normalized
                        FROM orb_companies.orb_companies_domains d INNER JOIN
                             orb_companies.normalized_companies c
                             USING(orb_num)
                        WHERE d.webdomain=%s''', domain)
                    if result:
                        record = self.cursor.fetchone()
                        normalized_record = record['normalized']

                        if self.find_with_weight(examined_names, normalized_record):
                            valid_result_success += 1
                        elif self.find_with_jaro(examined_names, normalized_record):
                            valid_result_jaro += 1
                        else:
                            valid_result_failed += 1

                    elif self.find_by_normalized(examined_names):
                        valid_no_result_success += 1
                    else:
                        valid_no_result_failed += 1

                elif self.find_by_normalized(examined_names):
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

            # match: 70.53% of our websites exists in orb database - this is ~41813
            # 5647 not valid, 53634 valid and from this 41813 exists in database
            # match: ORIGINAL name VS. name: ratio 0.80: 14926
            # match: ORIGINAL name VS. name: ratio 0.70: 20925
            # match: ORIGINAL name VS. name: ratio 0.50: 33738

            # match: ORIGINAL normalized name VS. normalized column, ratio 0.80: 23514
            # match: ORIGINAL normalized name VS. normalized column, ratio 0.70: 26972
            # match: ORIGINAL normalized name VS. normalized column, ratio 0.50: 33738

            # match: CLEANED normalized name VS. normalized column, ratio 0.80: 25456
            # match: CLEANED normalized name VS. normalized column, ratio 0.70: 28395
            # match: CLEANED normalized name VS. normalized column, ratio 0.60: 31196
            # match: CLEANED normalized name VS. normalized column, ratio 0.50: 33976

            # match: CLEANED NAME LIST normalized VS. normalized col, ratio 0.80: 26448 (+ simple: 26565)
            # match: CLEANED NAME LIST normalized VS. normalized col, ratio 0.70: 29511 (+ simple: 29619)
            # match: CLEANED NAME LIST normalized VS. normalized col, ratio 0.60: 32393 (+ simple: 32529)
            # match: CLEANED NAME LIST normalized VS. normalized col, ratio 0.50: 35178 (+ simple: 35330, + registry 35835)


    def query_with_normalized(self):

        success = 0
        with open(self.cleaned_file, 'rt') as candidates:
            reader = csv.DictReader(candidates)

            for row in reader:
                names_count = 0
                cleaned_names = row['cleaned_name']
                cleaned_names_list = cleaned_names.split('\t')
                examined_cleaned = cleaned_names_list[0]
                normalized_cleaned_name = self.normalize_name(examined_cleaned)

                result = self.cursor.execute\
                    ("SELECT name, normalized FROM orb_companies.normalized_companies WHERE normalized=%s",
                     normalized_cleaned_name)
                names_count += 1
                if result:
                    record = self.cursor.fetchone()
                    success += 1
                    if success % 500 == 0:
                        print(normalized_cleaned_name, record['normalized'])
        print(success)

        # match ORIGINAL normalized name VS. normalized column:
            # 28435 from 59282(all) (overall 47.96%)
        # match cleaned FIRST candidate vs. normalized column:
            # 36541 from 59282(all) (overall 61.63%)
        # match cleaned FIRST OR SECOND, depending on SECOND EXISTING vs. normalized column:
            # 36304 from 59282(all)
        # match cleaned NTH name, IF EXISTS:
            # 39085

    def load_csv(self):

        with open('files/orb_companies_names.csv', 'rt') as input_file:
            reader = csv.DictReader(input_file)
            with open('files/normalized_names.csv', 'wt') as results:
                writer = csv.DictWriter(results,
                                        fieldnames=['orb_num', 'name', 'normalized'])
                writer.writeheader()

                for row in reader:
                    normalized_name = row['name']
                    normalized_name = normalized_name.strip()
                    normalized_name = self.normalize_name(normalized_name)

                    writer.writerow({'orb_num': row['orb_num'], 'name': row['name'], 'normalized': normalized_name})



