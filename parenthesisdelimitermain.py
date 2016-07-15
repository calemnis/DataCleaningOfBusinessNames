#!usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import csv
import re

delimited_list = [] #this will contain other lists

def split_by_delimiters(line):
    """
    This function splits a line by various delimiters.
    Then strips the leading and trailing whitespaces.
    Then filters the returned list of strings for empty strings.
    """
    strings_list = sentence_delimiter_split(line)
    strings_list = clean_from_spaces(strings_list)
    return strings_list


def split_by_single_characters(item):
    """
    This function splits a line by single characters, mainly brackets.
    Then strips the leading and trailing whitespaces.
    Then filters the returned list of strings for empty strings.
    """
    split_list_item = single_characters_split(item)
    split_list_item = clean_from_spaces(split_list_item)
    return split_list_item


def apply_delimiters_to_stringlist(strings_list):
    """
    Input is a list of strings, the called function runs over all items of the list.
    Creates a new list, then extends it with the split items from the former list
    """
    new_strings_list = []
    for item in strings_list:
        split_list_item = split_by_single_characters(item)
        new_strings_list.extend(split_list_item)
    return new_strings_list


def clean_from_spaces(strings_list):

    strings_list = [x.strip() for x in strings_list]
    strings_list = [x for x in strings_list if x]
    return strings_list


def sentence_delimiter_split(stringexpr):
    return re.split(r'\s[,/-]\s|\*{2,}|\\{2,}|-{2,}|(?<!http:)//|(?<=\s)[-/](?=\w)|(?<=\w)/(?=\s)|(?<=[a-zA-Z]),(?=[a-zA-Z])', stringexpr)


def single_characters_split(stringexpr):
    return re.split(r'[()\[\]–|]', stringexpr)


if __name__ == '__main__':

    with open(sys.argv[1], 'rt') as csvfile:
        csvreader = csv.reader(csvfile, delimiter='\t')
        for row in csvreader:
            new_element = split_by_delimiters(''.join(row))
            new_element = apply_delimiters_to_stringlist(new_element)
            print(new_element)
            delimited_list.append(new_element)
            #print(new_element)

