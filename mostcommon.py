#!/usr/bin/env python3
# -*- coding: utf8 -*-

import csv
import sys
from collections import Counter


def is_special(char):
    return not char.isalnum() and not char.isspace()

if __name__ == '__main__':

    with open(sys.argv[1], 'rt') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter='\t')
        Chars = Counter()
        for row in csvreader:
            for c in filter(is_special, row['company_registration_name']):
                Chars[c] += 1

    for char, count in Chars.most_common(20):
        print(char, '\t', count)

