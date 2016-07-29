#!usr/bin/env python3
# -*- coding: utf8 -*-

import sys
import csv

if __name__ == '__main__':

    with open(sys.argv[1], 'rt') as csvinputfile, open('filtered_regnames_every_tenth.tsv', 'w') as outputfile:
        csvreader = csv.reader(csvinputfile, delimiter='\t')

        first_line = csvinputfile.readline()
        #first_line = first_line.split('\t')
        #first_item = first_line[1]
        outputfile.write(first_line)

        name_regname_list = []

        for row in csvreader:
            name_regname_list.append(row[0] + '\t' + row[1])

        name_regname_list = name_regname_list[0::10]
        for item in name_regname_list:
            outputfile.write(item + '\n')

