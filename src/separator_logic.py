#!/usr/local/bin python3
# -*- coding: utf-8 -*-

import sys
import re

cleaned_list = [] #this will contain other lists
stop_phrases_list = []

#TODO
#continue identificate the junk cases
#filter meltwater buzz
#more tests for negative and positive junk cases
#think about small junks, strings left little special characters like **, #, ^, -, etc
#home work from David! rest api - queries can be multiple
#grep


def clean_whitespaces(item, regex):
    item = regex.sub('', item)
    item = item.strip()
    return item


def strip_elements(strings_list):

    regex = re.compile(r'\\t$')
    strings_list = [clean_whitespaces(x, regex) for x in strings_list]
    strings_list = [x for x in strings_list if x]
    return strings_list


def separate_elements(line):

    #TODO
    #last task:
    #renaming values, func names
    #can THIS function be more efficient - strings_list passing all the time may be a problem, etc.

    strings_list = split_by_delimiters(line.strip())
    #examine_matches(strings_list)
    strings_list = filter_redundant(strings_list)
    strings_list = filter_sales_notes(strings_list)
    strings_list = strip_elements(strings_list)
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


def filter_redundant(strings_list):

    #regular expression to match business names where time zone is included
    timezone_pattern = re.compile(r"""

        ^([ECMP]ST)$            #in most matches the list item contained only the timezone
        |
        .*(\W[ECMP]ST)          #non-word character necessary, otherwise we get 'UB C TEST' to match

    """, flags=re.VERBOSE)

    #regular expression to extract the company value
    company_value_pattern = re.compile(r"""

        ^.*?                    #lazy match, expressions not necessary for capturing the company value
        (                           #we strive to extract company value with grouping
            (?<!\w)                 #we would like to avoid matching business names where 'some number' + 'K'
                                    #is part of the name
                \d+\.?\d*\s?[Kk]     #a number (may be decimal) and character K, space between them is optional

            (?!\w)
        )
        .*$                    #characters after the company value are not interesting for us

    """, flags=re.VERBOSE)

    strings_list = [re.sub('([ECMP]ST)', '', item, count=1) if timezone_pattern.match(item) else
                    re.sub(company_value_pattern.match(item).group(1), '', item) if company_value_pattern.match(item) else
                    item for item in strings_list]

    return strings_list


def clean_sales_notes(item):

    for phrase in stop_phrases_list:
        phrase_regex = re.compile(r'\b' + phrase + r'\b', flags=re.IGNORECASE)
        item = phrase_regex.sub('', item)
    return item


def filter_sales_notes(strings_list):

    #TODO
    #write tests for this

    strings_list = [clean_sales_notes(item) for item in strings_list]
    return strings_list


#For own purposes, identification, testing, etc.
# def examine_matches(strings_list):
#
#     regex1 = re.compile(r'^.*?(\d+\.?\d*\s?[k]).*$', re.IGNORECASE)
#     new_list1 = [m.group(0) for l in strings_list for m in [regex1.search(l)] if m]
#     if new_list1:
#         print(new_list1)


if __name__ == '__main__':

    with open('stop_phrases.txt', 'r') as stop_phrases:
        for phrase in stop_phrases:
            stop_phrases_list.append(phrase.strip())

    with open(sys.argv[1], 'rt') as input_file:
        for row in input_file:
            new_element = separate_elements(row)

            #print(new_element)
            cleaned_list.append(new_element)


