#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pymysql.cursors
import csv
import re
import tldextract
import validators
import unicodedata
import string
from cleaner.extension_cleaner import CompanyExtensionCleaner

class NameValidator:

    def __init__(self, websites_file):
        self.websites_file = websites_file

        self.connection = pymysql.connect(host='localhost', user='root', passwd='', db='orb_companies', charset='utf8')
        self.cursor = self.connection.cursor()
        self.extension_cleaner = CompanyExtensionCleaner('files/company_extensions.txt')

    def is_valid(url):
        return validators.url(url)

    def not_ascii(s):
        return all(ord(c) > 128 for c in s)

    def normalize_name(self, name):

        name = self.extension_cleaner.filter_extensions(name)
        name = name.lower()
        name = ''.join(name.split())
        exclude = set(string.punctuation)
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
                normalized = self.normalize_site(website)

                if NameValidator.is_valid(website):
                    extracted = tldextract.extract(normalized)
                    domain = extracted.registered_domain

                    result = self.cursor.execute("SELECT webdomain FROM orb_companies.orb_companies_domains WHERE webdomain=%s", domain)
                    if result:
                        success += 1
                        if success > 2000:
                            break
                        self.cursor.execute("SELECT orb_num FROM orb_companies.orb_companies_domains WHERE webdomain=%s", domain)
                        orb_num = self.cursor.fetchone()[0]

                        self.cursor.execute("SELECT name FROM orb_companies.orb_companies WHERE orb_num=%s", orb_num)
                        entry = self.cursor.fetchone()[0]

                        # TODO rather get a normalized name; make new column
                        original = entry
                        norm = self.normalize_name(entry)
                        if any(NameValidator.not_ascii(n) for n in original):

                            print(original)
                            print(norm)

            # now 61 % on all accounts
            print(success)

    def query_with_normalized(self):

        success = 0
        with open(self.websites_file, 'rt') as accounts:
            reader = csv.DictReader(accounts, delimiter='\t')

            for row in reader:
                # TODO not only name, but regname, cleaned name, etc.
                name = row['name']
                norm_name = self.normalize_name(name)
                result = self.cursor.execute("SELECT name FROM orb_companies.orb_1000 WHERE normalized=%s", norm_name)
                if result:
                    entry = self.cursor.fetchone()[0]
                    print(entry)
                    print(norm_name)
                    success += 1
        print(success)

    def iter_row(self, size=1000):
        while True:
            rows = self.cursor.fetchmany(size)
            if not rows:
                break
            for row in rows:
                yield row

    def make_normalize(self):

        for i in range(1, 550):
            step = 1000
            self.cursor.execute("SELECT name FROM filtered_companies29 LIMIT %s,1000", i*step)
            for row in self.iter_row(step):
                name = row[0]
                normalized = self.normalize_name(name)
                # TODO Why is this an occurrence?
                if not normalized:
                    print('this entry is not normalized - empty')

                self.cursor.execute("UPDATE filtered_companies29 SET normalized=%s WHERE name=%s", (normalized, name))
                self.connection.commit()

        # 550K data:
        # running time: 8-10 minutes


