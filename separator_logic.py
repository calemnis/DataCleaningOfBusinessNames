#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os.path
import re
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.cleaner.note_cleaner import NotesCleaner
from src.cleaner.country_cleaner import CountriesCleaner
from src.init import config

cleaned_list = [] #this will contain other lists

#TODO
#decide which country cases should be filtered and by what means:
#country subproblem: Random BusinessName TW/HK/JP?

#konfidentiellt, konzerlösung, other foreign language expressions
#same pattern is in parentheses
#dach

#think about small junks, strings left little special characters like **, #, ^, !!!!!, -, one letters (c), etc

#all the time renaming values, func names!
#filter redundant - module regex, pythex, PCRE library may improve readability

#home work from David! rest api - queries can be multiple
#grep


def separate_elements(line):

    print(line.strip())
    line = cut_redundant(line.strip())
    strings_list = split_by_delimiters(line)
    cleaned_strings_list = []
    for item in strings_list:
        item = filter_redundant(item)
        item = cleaner.filter_sales_notes(item)
        item = countries_cleaner.filter_alone_countries(item)
        cleaned_strings_list.append(item)

    strings_list = strip_elements(cleaned_strings_list)
    print(strings_list)

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

    cleaner = NotesCleaner('files/stop_phrases.txt')
    countries_cleaner = CountriesCleaner('files/country_table.csv', 'files/state_table.csv')

    with open(sys.argv[1], 'rt') as input_file:
        for row in input_file:
            new_element = separate_elements(row)

            #print(new_element)
            #cleaned_list.append(new_element)
