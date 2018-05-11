#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    File name : test_core_parse.py
    Description : testing initial functions parsing config files
    Author : Clément CHOUKROUN, Alexandre MOURACHKO
    Date created : 2018/04/18
    Python Version : 3.6
"""

import pytest
from xwords.core_parse import parse_input, populate_entry_dicts

lines_cleaned = parse_input("./xwords/tests/input_test.txt")
intents, entities, aliases = populate_entry_dicts(lines_cleaned)


def test_parse_input_empty():
    lines_empty = parse_input("./xwords/tests/input_empty.txt")
    assert len(lines_empty) == 1


def test_parse_input_1():
    assert len(lines_cleaned) == 5


def test_parse_input_2():
    assert lines_cleaned[1][1] == "this month"


def test_populate_entry_dicts_i1():
    assert len(intents) == 2


def test_populate_entry_dicts_i2():
    assert intents[0] == "Total number of @[subject_filter] ~[owners]"


def test_populate_entry_dicts_empty():
    lines_empty = parse_input("./xwords/tests/input_empty.txt")
    int_0, ent_0, ali_0 = populate_entry_dicts(lines_empty)
    assert (len(int_0) == 0) & (len(ent_0) == 0) & (len(ali_0) == 0)


def test_populate_entry_dicts_e1():
    assert len(entities) == 3


def test_populate_entry_dicts_e2():
    assert list(entities.keys())[2] == "@[subject_filter]"


def test_populate_entry_dicts_e3():
    assert len(list(entities.values())[1]) == 7


def test_populate_entry_dicts_e4():
    assert list(entities.values())[1][3] == "United States"


def test_populate_entry_dicts_a1():
    assert len(aliases) == 1


def test_populate_entry_dicts_a2():
    assert list(aliases.keys())[0] == "~[owners]"


def test_populate_entry_dicts_a3():
    assert len(list(aliases.values())[0]) == 2


def test_populate_entry_dicts_a4():
    assert list(aliases.values())[0][1] == "possessors"
