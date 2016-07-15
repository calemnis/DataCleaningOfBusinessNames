#!usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re

delimited_list = [] #this will contain other lists


def clean_from_spaces(strings_list):

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
    return re.split(r'\s[,/-]\s|(?<!http:)//|(?<=\s)[-/](?=\w)|(?<=\w)/(?=\s)|(?<=[a-zA-Z]),(?=[a-zA-Z])|[\(\)\[\]\–\|]|\*{2,}|\\{2,}|-{2,}', stringexpr)


if __name__ == '__main__':

    with open(sys.argv[1], 'rt') as input_file:
        for row in input_file:
            new_element = split_by_delimiters(row)
            print(new_element)
            delimited_list.append(new_element)
            #print(new_element)

