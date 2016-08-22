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

# TODO #1 check query_with_normalized
# TODO #2 validate with the help of the new normalized column - website
# TODO #3 orb_companies_names port to table and foreign key orb_num

URLs_list = []
Cleaned_query_list = []


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

    def not_ascii(s):
        return all(ord(c) > 128 for c in s)

    def get_ratio(self, first, second):
        return Levenshtein.ratio(first, second)

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

    def get_url_correspondence(self):
        success = 0

        with open(self.cleaned_file, 'rt') as candidates:
            reader = csv.DictReader(candidates)

            for row in reader:
                website = row['website']
                cleaned_names = row['cleaned_name']
                simple_name = row['name']

                normalized_website = self.normalize_site(website)
                cleaned_names_list = cleaned_names.split('\t')
                examined_cleaned = cleaned_names_list[0]
                normalized_cleaned_name = self.normalize_name(examined_cleaned)

                if NameValidator.is_valid(website):
                    extracted = tldextract.extract(normalized_website)
                    domain = extracted.registered_domain

                    result = self.cursor.execute('''
                        SELECT name, normalized
                        FROM orb_companies.orb_companies_domains d INNER JOIN
                             orb_companies.normalized_companies c
                             USING(orb_num)
                        WHERE d.webdomain=%s''', domain)
                    if result:
                        record = self.cursor.fetchone()
                        ratio = self.get_ratio(normalized_cleaned_name, record['normalized'])
                        if ratio > 0.50:
                            success += 1
                            URLs_list.append(record['normalized'])
                            # if success % 500 == 0:
                            #     print(normalized_cleaned_name, record['name'])
                        else:
                            if success % 100 == 0:
                                print(ratio, simple_name, '\t', record['name'], '\t', normalized_cleaned_name, record['normalized'])

            print(success)
            # match: 61% of our websites exists in orb database - this is ~36162 (overall 60.99%)
            # match: ORIGINAL name VS. name: 12984 is over 0.85 levenshtein ratio from ~36162 (35.905%, overall 21.902%)
            # match: ORIGINAL name VS. name: 14736 is over 0.80 levenshtein ratio from ~36162 (40.749%, overall 24.85%)

            # match: ORIGINAL normalized name VS. normalized column, levenshtein ratio 0.80:
                # 20507 from ~36162 (overall 34.592%)
            # match: CLEANED normalized name VS. normalized column, levenshtein ratio 0.80:
                # 22187 from ~36162
            # match: CLEANED normalized name VS. normalized column, levenshtein ratio 0.75:
                # 23437
            # match: CLEANED normalized name VS. normalized column, levenshtein ratio >=0.60:
                # 27350
            # match: CLEANED normalized name VS. normalized column, levenshtein ratio >0.50:
                # 29644

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
                    Cleaned_query_list.append(record['normalized'])
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

    def unique(self, a):
        return len(set(a))

    def diff(self, first, second):
        return len(set(first) - set(second))

    def get_union(self):
        print("I am the urls list. Want to know How unique am I?", "But first my length: ", len(URLs_list))
        print("This unique you dumbheads:", self.unique(URLs_list))

        print("I am the simple cleaned names queries list. How unique am I?", "First my length:",
              len(Cleaned_query_list))
        print("This unique you dumbheads:", self.unique(Cleaned_query_list))

        print("Our intersection is", len(set(URLs_list) & set(Cleaned_query_list)), "long")
        print("Our union is", len(set(URLs_list) | set(Cleaned_query_list)), "long")

        print("Our difference is...", self.diff(URLs_list, Cleaned_query_list),
              self.diff(Cleaned_query_list, URLs_list))

        #regarding intersection of the two sets (urls and simple search by cleaned normalized name):
            # match cleaned FIRST candidate vs. normalized column:
                # 36541 from 59282(all) (overall 61.63%)
            # match: CLEANED normalized name VS. normalized column, levenshtein ratio 0.80:
                # 22187 from ~36162 (overall 61.354%)

            # I am the urls list. Want to know How unique am I? But first my length:  22187
            # This unique you dumbheads: 21573
            # I am the simple cleaned names queries list. How unique am I? First my length: 36541
            # This unique you dumbheads: 34640
            # Our intersection is 16999 long
            # Our union is 39214 long
            # Our difference is...   4574 17641

    def make_normalize(self):
        success = 0
        step = 1000
        for i in range(0, 520000, step):
            self.connection.begin()
            self.cursor.execute("SELECT orb_num, name FROM filtered_companies29 ORDER BY orb_num LIMIT %s,%s", (i, step))
            for row in self.cursor.fetchall():
                normalized = self.normalize_name(row['name'])
                if not normalized:
                    print(row, 'this entry is not normalized - empty')
                self.cursor.execute("UPDATE filtered_companies29 SET normalized=%s WHERE name=%s", (normalized, row['name']))
                success += 1
            self.connection.commit()
        print(success)

    def load_csv(self):

        with open('files/filtered_companies.csv', 'rt') as input_file:
            reader = csv.DictReader(input_file)
            with open('files/normalized_companies.csv', 'wt') as results:
                writer = csv.DictWriter(results,
                                        fieldnames=['orb_num', 'name', 'state', 'country', 'normalized'])
                writer.writeheader()

                for row in reader:
                    normalized_name = row['name']
                    normalized_name = normalized_name.strip()
                    normalized_name = self.normalize_name(normalized_name)

                    writer.writerow({'orb_num': row['orb_num'], 'name': row['name'], 'state': row['state'],
                                    'country': row['country'], 'normalized': normalized_name})



