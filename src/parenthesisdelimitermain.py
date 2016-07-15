#!usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re

delimited_list = [] #this will contain other lists


def clean_from_spaces(strings_list):

    strings_list = [x.strip("\t") for x in strings_list]
    strings_list = [x.strip() for x in strings_list]
    strings_list = [x for x in strings_list if x]
    return strings_list


def split_by_delimiters(line):
    """
    This function splits a line by various delimiters.
    Then strips the leading and trailing whitespaces.
    Then filters the returned list of strings for empty strings.
    """
    strings_list = sentence_delimiter_split(line)
    strings_list = clean_from_spaces(strings_list)
    return strings_list


def sentence_delimiter_split(stringexpr):
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


if __name__ == '__main__':

    with open(sys.argv[1], 'rt') as input_file:
        for row in input_file:
            new_element = split_by_delimiters(row)
            print(new_element)
            delimited_list.append(new_element)
            #print(new_element)

