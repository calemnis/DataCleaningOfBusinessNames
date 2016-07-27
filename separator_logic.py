#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os.path
import re
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.cleaner.note_cleaner import NotesCleaner
from src.init import config

cleaned_list = [] #this will contain other lists
countries_set = []
i = 0

#TODO
#continue identificate the junk cases
#examine cardinality of occurring country names, mainly whole names

#decide which country cases should be filtered and by what means:
#regexes only?
#regexes firstly for subproblems, like Random BusinessName TW/HK/JP?

#some smaller cases: formerly (281 cases), ehemals, ehem., ehemalige, migrated, many types of licence...
#...migrated (stop word now), konfidentiellt, konzerlösung, other foreign language expressions
#there may be sales notes not yet discovered

#think about small junks, strings left little special characters like **, #, ^, !!!!!, -, etc

#renaming values, func names
#filter redundant - module regex, pythex, PCRE library may improve readability

#home work from David! rest api - queries can be multiple
#grep


def separate_elements(line):

    #print(line.strip())
    strings_list = split_by_delimiters(line.strip())

    cleaned_strings_list = []
    for item in strings_list:
        item = filter_redundant(item)
        item = cleaner.filter_sales_notes(item)
        cleaned_strings_list.append(item)

    strings_list = strip_elements(cleaned_strings_list)
    #print(strings_list)
    return strings_list


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
            item = re.sub(search_obj.group(0), '', item)
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


# def filter_countries(strings_list):
#
#     for item in strings_list:
#         text = item.split()
#         for word in text:
#

# def examine_matches(strings_list):
#
#     regex1 = re.compile(r'\b\w{2}([//,]\w{2})+\b', re.IGNORECASE)
#     new_list1 = [m.group(0) for l in strings_list for m in [regex1.search(l)] if m]
#     if new_list1:
#         print(new_list1)


if __name__ == '__main__':

    cleaner = NotesCleaner('files/stop_phrases.txt')

    countries_list = []
    with open('country.csv', 'r') as countries:
        [countries_list.extend([key, value.strip()]) for key, value in (item.split(',') for item in countries)]
        countries_set = frozenset(countries_list)

    with open(sys.argv[1], 'rt') as input_file:
        for row in input_file:
            new_element = separate_elements(row)

            #print(new_element)
            cleaned_list.append(new_element)
