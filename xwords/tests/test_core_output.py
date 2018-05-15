#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    File name : test_core_output.py
    Description : checking late stage functions outputing results
    Author : Clément CHOUKROUN
    Date created : 2018/04/18
    Python Version : 3.6
"""

import pytest
from xwords.core_output import generate

input_path = "./xwords/tests/input_test.txt"
input_path_empty = "./xwords/tests/input_empty.txt"


# Rasa NLU file
@pytest.fixture(scope='session')
def output_file(tmpdir_factory):
    fn = tmpdir_factory.mktemp('output')
    generate(input_path, output_path=str(fn), training_ratio=1.0, n_sub=None,
             for_story=False)
    return fn + 'training.md'


# empty Rasa NLU file
@pytest.fixture(scope='session')
def output_file_empty(tmpdir_factory):
    fn = tmpdir_factory.mktemp('output')
    generate(input_path_empty, output_path=str(fn), training_ratio=1.0,
             n_sub=None, for_story=False)
    return fn + 'training.md'


# rasa Core File
@pytest.fixture(scope='session')
def output_file_story(tmpdir_factory):
    fn = tmpdir_factory.mktemp('output')
    generate(input_path, output_path=str(fn), training_ratio=1.0, n_sub=100,
             for_story=True)
    return fn + 'training.md'


# empty rasa Core file
@pytest.fixture(scope='session')
def output_file_empty_story(tmpdir_factory):
    fn = tmpdir_factory.mktemp('output')
    generate(input_path_empty, output_path=str(fn), training_ratio=1.0,
             n_sub=None, for_story=True)
    return fn + 'training.md'


# Rasa NLU file - with testing set
@pytest.fixture(scope='session')
def output_file_testset(tmpdir_factory):
    fn = tmpdir_factory.mktemp('output')
    generate(input_path, output_path=str(fn), training_ratio=.7, n_sub=None,
             for_story=False)
    return fn + 'training.md'


# rasa Core File - with testing set
@pytest.fixture(scope='session')
def output_file_story_testset(tmpdir_factory):
    fn = tmpdir_factory.mktemp('output')
    generate(input_path, output_path=str(fn), training_ratio=.7, n_sub=100,
             for_story=True)
    return fn + 'training.md'


# testing number of lines returned in case of empty config file
def test_generate_empty(output_file_empty):
    with open(output_file_empty, 'r') as generated_file:
        assert sum((1 for l in generated_file)) == 0


def test_generate_empty_story(output_file_empty_story):
    with open(output_file_empty_story, 'r') as generated_file:
        assert sum((1 for l in generated_file)) == 0


# testing number of lines returned
def test_generate(output_file):
    with open(output_file, 'r') as generated_file:
        assert sum((1 for l in generated_file)) == 684


# testing number of lines returned
def test_generate_story(output_file_story):
    with open(output_file_story, 'r') as generated_file:
        assert sum((1 for line in generated_file if line[0:2] == "##")) == 100


# testing number of lines returned
def test_generate_testset(output_file_testset):
    with open(output_file_testset, 'r') as generated_file:
        assert sum((1 for l in generated_file)) == 478


# testing number of lines returned
def test_generate_story_teset(output_file_story_testset):
    with open(output_file_story_testset, 'r') as generated_file:
        assert sum((1 for line in generated_file if line[0:2] == "##")) == 70
