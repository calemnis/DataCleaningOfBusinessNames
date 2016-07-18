#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re

delimited_list = [] #this will contain other lists


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

    strings_list = split_by_delimiters(line.strip())
    strings_list = filter_timezones(strings_list)
    strings_list = strip_elements(strings_list)
    return strings_list


def split_by_delimiters(stringexpr):
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
        """, stringexpr, flags=re.IGNORECASE|re.VERBOSE)


def filter_timezones(strings_list):

    regex_pattern = re.compile(r"""
        ^([ECMP]ST)$            #in most matches the list item contained only the timezone
    |   .*(\W[ECMP]ST)          #non-word character necessary, otherwise we get 'UB C TEST' to match
    |   ^([ECMP]ST\W).*
    """, flags=re.IGNORECASE)

    print(strings_list)
    strings_list = [re.sub('([ECMP]ST)', '', item) if regex_pattern.match(item) else item for item in strings_list]

    return strings_list


if __name__ == '__main__':

    with open(sys.argv[1], 'rt') as input_file:
        for row in input_file:
            new_element = separate_elements(row)

            print(new_element)
            delimited_list.append(new_element)



