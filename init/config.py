#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re


results = ''


def get_results_file():
    if results is not None:
        return results
    else:
        raise ValueError('Value of results file is not set.')

patterns = set()
cutpatterns = set()

#regular expressions to match business names where time zone is included
timezone_pattern_alone = re.compile(r'^[ECMP][SD]T$')

timezone_pattern = re.compile(r"""

        \W[ECMP][SD]T          #non-word character necessary, otherwise we get 'UB C TEST' to match

""", flags=re.VERBOSE)

#regular expression to extract the company value
company_value_pattern = re.compile(r"""

        (?<!\w)                 #we would like to avoid matching business names where 'some number' + 'K'
                                #is part of the name
            \d+\.?\d*\s?[Kk]     #a number (may be decimal) and character K, space between them is optional

        (?!\w)

""", flags=re.VERBOSE)

notes_pattern = re.compile(r'\W?\w+\s(portion|license)', flags=re.IGNORECASE)

buzz_pattern = re.compile(r"""

        \W?
        (www)?               #website may start with www
        (http://)?           #also with http://
        (services)?
        \.meltwaterbuzz
        .*                   #every information after website name is captured and gets deleted.
                             #usernames, passwords, etc.
""", flags= re.VERBOSE)

formerly_pattern = re.compile(r'\W?(former|ehem|tidl).*', flags=re.IGNORECASE)

countries_junk_pattern = re.compile(r'(?<!\w)(\w{2})([,/]\s?\w{2})+(?!\w)')

patterns.update({timezone_pattern_alone, timezone_pattern, company_value_pattern, notes_pattern})

cutpatterns.update({formerly_pattern, buzz_pattern})