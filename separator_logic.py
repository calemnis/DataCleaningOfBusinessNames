#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import os.path
import re
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from cleaner.note_cleaner import NotesCleaner
from cleaner.country_cleaner import CountriesCleaner
import config
from runner.spider_runner import SpiderRunner

import ahocorasick

#TODO
#konfidentiellt, konzerlösung, other foreign language expressions
#same pattern is in parentheses
#dach

#think about small junks, strings left little special characters like **, #, ^, !!!!!, -, one letters (c), etc

#all the time renaming values, func names!
#filter redundant - module regex, pythex, PCRE library may improve readability

#home work from David! rest api - queries can be multiple
#grep


def separate_elements(line):

    line = cut_redundant(line.strip())
    strings_list = split_by_delimiters(line)
    cleaned_strings_list = []
    for item in strings_list:
        item = filter_redundant(item)
        item = cleaner.filter_sales_notes(item)
        item = countries_cleaner.filter_alone_countries(item)
        #clean_small_junk(item)
        cleaned_strings_list.append(item)

    strings_list = strip_elements(cleaned_strings_list)

    return strings_list


def cut_redundant(expression):

    for pattern in config.cutpatterns:
        search_obj = pattern.search(expression)
        if search_obj:
            expression = re.sub(re.escape(search_obj.group(0)), r'', expression)

    return expression


def split_by_delimiters(expression):

    return re.split(r"""
            \s[,/-]\s            #parenthesis, slash, hyphen starting/ending with spaces
        |   (?<!http:) //             #double slash, but only if behind no 'http:' expression
        |   (?<=\s) [-/] (?=\w)            #hyphen and slash, if there is a space behind and word character after
        |   (?<=\w)  /  (?=\s)             #matches a slash if word character behind and followed by space
        |   (?<=[a-zA-Z]) , (?=[a-zA-Z])   #matches the comma, but only if between word characters, except numbers
        |   [\(\)\[\]\–\|]                 #matches various brackets, vertical line and emdash
        |   \*{2,}                    #matches two or more star characters
        |   \\{2,}               #matches two or more backslashes
        |   -{2,}            #matches two or more hyphens
        """, expression, flags=re.VERBOSE)


def filter_redundant(item):

    for pattern in config.patterns:
        search_obj = pattern.search(item)
        if search_obj:
            item = re.sub(re.escape(search_obj.group(0)), r'', item)
    return item


def strip_elements(strings_list):

    regex = re.compile(r'\\t$')
    strings_list = [clean_whitespaces(x, regex) for x in strings_list]
    strings_list = [x for x in strings_list if x]
    return strings_list


def clean_whitespaces(item, regex):
    item = regex.sub('', item)
    item = item.strip()
    return item

if __name__ == '__main__':

    full_clean = False
    cleaner = NotesCleaner('files/stop_phrases.txt')
    countries_cleaner = CountriesCleaner('files/countries_table.csv')

    with open(sys.argv[1], 'rt') as input_file:

        reader = csv.DictReader(input_file, delimiter='\t')
        if len(reader.fieldnames) == 4:
            full_clean = True

        if full_clean:

            results_file = 'files/cleaned_businessnames.csv'
            config.results = results_file

            with open(results_file, 'wt') as results:

                writer = csv.DictWriter(results, fieldnames=['account_id', 'name', 'company_registration_name', 'cleaned_name'])
                writer.writeheader()
                spider_runner = SpiderRunner(raw_data_file=sys.argv[1])

                for row in reader:

                    cleaned_business_name = separate_elements(row['name'])
                    writer.writerow({'account_id': row['account_id'],
                                    'name': row['name'], 'company_registration_name': row['company_registration_name'],
                                     'cleaned_name': '\t'.join(cleaned_business_name)})

                spider_runner.run_spider()
                #ahocorasick.download()


        else:
            for row in reader:
                print(row['name'])
                cleaned_business_name = separate_elements(row['name'])
                print(cleaned_business_name)
