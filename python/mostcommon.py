#!/usr/bin/env python3
import csv
import sys
from collections import Counter
from mostcommonlib import is_special

with open(sys.argv[1], 'rt') as csvfile:
    csvreader = csv.DictReader(csvfile, delimiter='\t')
    Chars = Counter()
    for row in csvreader:
        for c in filter(is_special, row['name']):
            Chars[c] += 1

for char, count in Chars.most_common(10):
    print(char, count)
