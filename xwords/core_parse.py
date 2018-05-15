#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    File name: core_parse.py
    Description: helper functions to parse input config file
    Author: Clément CHOUKROUN, Alexandre MOURACHKO
    Date created: 2018/04/26
    Python Version: 3.6
"""

import re


def parse_input(input_path):
    """
    Summary
    ----------
    Parsing input config file and creating list of paragraphs (lists of lines)

    Parameters
    ----------
    input_path:
        path to config file

    Returns
    -------
    List
        List (one element for each paragraph) of lists (one element for each
        line within the paragraph)

    """

    with open(input_path, mode='r') as input_file:
        text = input_file.read().rstrip()

    # splitting raw text file into paragraphs
    # paragraphs are separated by at least 2 new lines
    # variable paragraphs is a list of strings (1 string = 1 paragraph)
    paragraphs = re.compile("\n{2,}").split(text)

    # splitting each paragraph into lines
    # variable lines is a list of lists of strings (1 string = 1 line)
    lines = [p.splitlines() for p in paragraphs]

    # removing space and tabs at beginning of lines
    lines_cleaned = [[line.lstrip() for line in p] for p in lines]

    return lines_cleaned


def populate_entry_dicts(lines_cleaned, grammar=None):
    """
    Summary
    ----------
    Classifies each line according to input grammar

    Parameters
    ----------
    lines_cleaned:
        List of lists as returned by parse_input
    grammar:
        list of keywords signaling configuration structure
        (entities, aliases, intents)


    Returns
    -------
    Tuple
        Composed of 3 elements (as designed for Rasa NLU):
        - intents_list
        - entities_dic
        - aliases_dic

    """

    if grammar is None:
        grammar = ["@", "~", "&"]
    intents_list = list()
    entities_dic = dict()
    aliases_dic = dict()

    # populating dicts by detecting first character of first line of
    # each paragraph
    try:
        for paragraph in lines_cleaned:
            if paragraph[0][0] == grammar[0]:
                entities_dic[paragraph[0]] = paragraph[1:]
            elif paragraph[0][0] == grammar[1]:
                aliases_dic[paragraph[0]] = paragraph[1:]
            else:
                intents_list.extend(paragraph)
    finally:
        return intents_list, entities_dic, aliases_dic
