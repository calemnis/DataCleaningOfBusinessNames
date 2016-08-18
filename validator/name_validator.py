#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pymysql.cursors
import csv
import re
import tldextract
import validators
import unicodedata
import string
import Levenshtein
from cleaner.extension_cleaner import CompanyExtensionCleaner

class NameValidator:

    def __init__(self, websites_file):
        self.websites_file = websites_file

        self.connection = pymysql.connect(host='localhost', user='root', passwd='', db='orb_companies', charset='utf8',
                                          cursorclass=pymysql.cursors.DictCursor,
                                          autocommit=False)
        self.cursor = self.connection.cursor()
        self.extension_cleaner = CompanyExtensionCleaner('files/company_extensions.txt')

    def is_valid(url):
        return validators.url(url)

    def not_ascii(s):
        return all(ord(c) > 128 for c in s)

    def get_ratio(self, first, second):
        return Levenshtein.ratio(first, second)

    def normalize_name(self, name):

        # TODO make foreign key
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

        with open(self.websites_file, 'rt') as accounts:
            reader = csv.DictReader(accounts, delimiter='\t')

            for row in reader:
                website = row['website']
                name = row['name']
                normalized = self.normalize_site(website)

                if NameValidator.is_valid(website):
                    extracted = tldextract.extract(normalized)
                    domain = extracted.registered_domain

                    result = self.cursor.execute('''
                        SELECT orb_num, name
                        FROM orb_companies.orb_companies_domains d INNER JOIN
                             orb_companies.orb_companies c
                             USING(orb_num)
                        WHERE d.webdomain=%s''', domain)
                    if result:
                        record = self.cursor.fetchone()
                        ratio = self.get_ratio(name, record['name'])
                        if ratio > 0.80:
                            success += 1


            # match: 61% of our websites exists in orb database - this is ~36162
            # match: simple name: 12984 is over 0.85 levenshtein ratio from ~36162 (35.905%)
            # match: simple name: 14736 is over 0.80 levenshtein ratio from ~36162 (40.749%)
            print(success)

    def query_with_normalized(self):

        success = 0
        with open(self.websites_file, 'rt') as accounts:
            reader = csv.DictReader(accounts, delimiter='\t')

            for row in reader:
                name = row['name']
                norm_name = self.normalize_name(name)
                result = self.cursor.execute("SELECT name FROM filtered_companies29 WHERE normalized=%s", norm_name)
                if result:
                    success += 1
        print(success)

    # TODO #0 make new column in orb_companies - normalized
    # TODO #1 check query_with_normalized
    # TODO #2 validate with the help of the new normalized column - website
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

