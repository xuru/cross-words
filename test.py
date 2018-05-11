#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    File name : test.py
    Description : quick and dirty first script
    Author : Clément CHOUKROUN, Alexandre MOURACHKO
    Date created : 2018/04/18
    Python Version : 3.6
"""

from xwords.core_output import generate

generate("./xwords/tests/input_test.txt", n_sub=100, for_story=False)
