#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    File name: core_process.py
    Description: helper functions to generate NLU/Core combinations across
                 intents, entities and aliases
    Author: Clément CHOUKROUN, Alexandre MOURACHKO
    Date created: 2018/04/26
    Python Version: 3.6
"""

import re
import itertools
import random
from .utils import unique, remove_grammar


def replace_in_str(sentence, key, value, for_story=False,
                   grammar=["%", "@", "~", "&"]):
    """
    Summary
    ----------
    Replacing part of sentence to comply with Rasa NLU/Core training structure

    Parameters
    ----------
    sentence:
        string to replace a part of
    key:
        string to use as key in the replacing scheme, which will also be
        replaced in the sentence
    value:
        string to use as value in the replacing scheme
    for_story:
        bool to indicate whether the replacement should be done according to
        Rasa Core scheme
    grammar:
        list of keywords signaling configuration structure
        (entities, aliases, intents)

    Returns
    -------
    List
        sentence with key replaced by either:
        - "key": "value" (Rasa Core training format)
        - [value](key) (Rasa NLU training format for entities)
        - value (Rasa NLU training format for aliases and intents)

    """

    if for_story:  # true if replacing for Rasa Core format
        # replacing key by "key": "value"
        replacement = "\"" + remove_grammar(key, grammar) + \
            "\": \"" + remove_grammar(value, grammar) + "\""
    else:  # Rasa NLU format
        if key[0] == grammar[1]:  # identifying an entity
            # replacing key by [value](key)
            replacement = "[" + value + "](" + \
                          remove_grammar(key, grammar) + ")"
        else:
            # replacing key by value
            replacement = value

    return sentence.replace(key, replacement)


def place_combinations(sentence, replacement_dic, for_story=False,
                       grammar=["%", "@", "~", "&"]):
    """
    Summary
    ----------
    Placing all combinations from a replacement dictionnary into a sentence

    Parameters
    ----------
    sentence:
        string to place combinations into
    replacement_dic:
        base dictionnary to generate combinations from
    for_story:
        bool to indicate whether the placement should be done according to
        Rasa Core scheme
    grammar:
        list of keywords signaling configuration structure
        (entities, aliases, intents)

    Returns
    -------
    List
        list of all combinations of replacement elements into the source
        sentence

    """

    # grammar_pattern = "[%@~&]\[w+\]" # for default grammar
    grammar_pattern = "[" + "".join(grammar) + r"]\[\w+\]"

    # getting placeholders in sentence while keeping order
    placeholder_list = [pos for pos
                        in re.compile(grammar_pattern).findall(sentence)
                        if pos in set(replacement_dic.keys())]
    placeholder_list = unique(placeholder_list)

    # create list of replacements to be inserted into placeholders
    placeholder_replacements = [replacement_dic[pos]
                                for pos in placeholder_list]

    # create all possible combinations of replacement values
    if for_story:
        # create one random combination of dict values
        combinations = [[random.choice(ls) for ls in placeholder_replacements]]
    else:
        # create all possible combinations of dict values
        combinations = list(itertools.product(*placeholder_replacements))

    output = list()

    for combi in combinations:
        sentence_mod = sentence
        # replacing regex matches by every possible value combination
        match_len = len(placeholder_list)
        if match_len >= 1:
            for i in range(match_len):
                sentence_mod = replace_in_str(
                    sentence_mod, placeholder_list[i], list(combi)[i],
                    for_story, grammar)
        output.append(sentence_mod)

    return output


def generate_sentences(intents_list, entities_dic, aliases_dic, n_sub=None,
                       grammar=["%", "@", "~", "&"]):
    """
    Summary
    ----------
    Generating full training and testing sets with all placeholder combinations
    for all source sentences. To be used for Rasa NLU only.

    Parameters
    ----------
    intents_list:
        list of all intents in source config file
    entities_dic:
        dictionnary of all entities in source config file, in the form
        "entity": [list of all variants of this entity]
    aliases_dic:
        dictionnary of all aliases in source config file, in the form
        "alias": [list of all variants of this alias]
    n_sub:
        number of randomly selected sentences to subsample from the total
        number of combinations. If None, returns the full set of sentence
        combinations.
    grammar:
        list of keywords signaling configuration structure
        (entities, aliases, intents)

    Returns
    -------
    List
        list of generated sentences

    """

    # building all combinations of entities x aliases
    entities_and_aliases = {**entities_dic, **aliases_dic}
    sentence_count = 0
    sentences = list()

    # generating all intent sentences with their combinative duplicates
    for intent_sentence in intents_list:
        # replace by every possible combination of entities and aliases
        combo_list = place_combinations(intent_sentence, entities_and_aliases,
                                        for_story=False, grammar=grammar)
        sentences.extend(combo_list)
        sentence_count = sentence_count + len(combo_list)
    print(sentence_count, "sentences generated")

    # returning a subsample of generated sentences if asked
    if n_sub is not None and n_sub < sentence_count:
        print(n_sub, "sentences selected out of", sentence_count)
        samp = sorted(random.sample(range(sentence_count), n_sub))
        return [sentences[k] for k in samp]
    else:
        return sentences


def generate_utter_actions(entities_dic, grammar=["%", "@", "~", "&"]):
    """
    Summary
    ----------
    Generating inquisitive replies for Rasa Core

    Parameters
    ----------
    entities_dic:
        dictionnary of all entities in source config file, in the form
        "entity": [list of all variants of that entity]

    Returns
    -------
    Dictionnary
        list of generated bot questions for all entities

    """

    actions_dic = dict()
    for key in entities_dic.keys():
        actions_dic[key] = "utter_ask_" + remove_grammar(key, grammar)

    return actions_dic


def generate_empty_story(intent_string, entities_dic, actions_dic):
    """
    Summary
    ----------
    Generating a single story with  empty placeholders for Rasa Core

    Parameters
    ----------
    intent_string:
        intent of the story to be generated
    entities_dic:
        dictionnary of entities to prepare placeholders for in intent_string
    actions_dic:
        dictionnary of actions as output by generate_utter_actions

    Returns
    -------
    String
        single story with empy placeholders

    """

    entities_len = len(entities_dic)

    # pick n random entities among the entities_len available in entities dict
    # n entities are asked in first user imput
    # n-entities_len are asked by the bot usin utter_ask_ actions
    # all entities in random order
    n = random.randint(0, entities_len)
    entities_input = random.sample(list(entities_dic.keys()), n)
    entities_asked = [ent for ent in entities_dic if ent not in entities_input]

    story = "## Genereated Story " + str(int(random.random()*10**15)) + "\n"
    story += "* " + intent_string + "{" + ', '.join(entities_input) + "}\n"

    for ent in entities_input:
        story += "    - slot{" + ent + "}\n"
    for ent in entities_asked:
        story += "    - " + actions_dic[ent] + "\n"
        story += "* " + intent_string + "{" + ent + "}\n"
        story += "    - slot{" + ent + "}\n"
    story += "    - action_" + intent_string + "\n"

    return story


def generate_stories(intent_string, entities_dic, n_sub,
                     grammar=["%", "@", "~", "&"]):
    """
    Summary
    ----------
    Generating all stories with their combinative duplicates for Rasa Core

    Parameters
    ----------
    intent_string:
        intent of the stories to be generated

    entities_dic:
        dictionnary of all entities to generate combinations
    n_sub:
        number of randomly created stories

    Returns
    -------
    List
        List of all generated stories with combinations placed

    """
    output_stories = list()

    if entities_dic != {}:
        actions = generate_utter_actions(entities_dic, grammar)
        for _ in range(0, n_sub):
            # generate one story with placeholders for entities
            single_story = generate_empty_story(intent_string, entities_dic,
                                                actions)
            # replace placeholders by random values picked in entities dict
            single_story = place_combinations(single_story, entities_dic,
                                              for_story=True)
            output_stories.extend(single_story)
        print(n_sub, "stories generated")

    return output_stories
