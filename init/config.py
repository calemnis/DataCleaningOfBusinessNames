#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

patterns = set()

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

buzz_pattern = re.compile(r"""

        \W?
        (www)?               #website may start with www
        (http://)?           #also with http://
        (services)?
        \.meltwaterbuzz
        .*                   #every information after website name is captured and gets deleted.
                             #usernames, passwords, etc.
""", flags= re.VERBOSE)

patterns.update({timezone_pattern_alone, timezone_pattern, company_value_pattern, buzz_pattern})