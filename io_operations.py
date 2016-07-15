#!usr/bin/env python3
# -*- coding: utf8 -*-

import sys
import csv

if __name__ == '__main__':

    with open(sys.argv[1], 'rt') as csvinputfile, open('business_names_only_every_tenth.csv', 'w') as outputfile:
        csvreader = csv.reader(csvinputfile, delimiter = '\t')

        first_line = csvinputfile.readline()
        first_line = first_line.split('\t')
        first_item = first_line[1]
        outputfile.write(first_item + '\n')

        business_list = []

        for row in csvreader:
            business_list.append(row[1])

        business_list = business_list[0::10]
        for item in business_list:
            outputfile.write(item + '\n')

