#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    File name : utils.py
    Description : global utility functions
    Author : Clément CHOUKROUN, Alexandre MOURACHKO
    Date created : 2018/04/18
    Python Version : 3.6
"""


def unique(sequence):
    """
    Summary
    ----------
    Removing duplicates in list while keeping order of item appearance

    Parameters
    ----------
    sequence:
        list to remove duplicates from

    Returns
    -------
        list with no duplicates, in the same order

    """

    seen = set()
    return [e for e in sequence if not (e in seen or seen.add(e))]


def remove_grammar(element, grammar=None):
    """
    Summary
    ----------
    Removing grammar keywords from sentence element

    Parameters
    ----------
    element:
        element to remove any grammar keyword from
    grammar:
        list of keywords signaling configuration structure
        (entities, aliases, intents)

    Returns
    -------
        element cleaned from any grammar keyword

    """
    if grammar is None:
        grammar = ["%", "@", "~", "&"]
    reg = "[" + "".join(grammar) + "]"
    return str.strip(element, reg)
