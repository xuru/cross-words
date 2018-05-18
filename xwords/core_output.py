#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    File name: core_output.py
    Description: helper functions to output results into text files
    Author: Clément CHOUKROUN, Alexandre MOURACHKO
    Date created: 2018/04/26
    Python Version: 3.6
"""

import os
import random
from .core_parse import parse_input, populate_entry_dicts
from .core_process import generate_sentences, generate_stories


def write_file(sentences, file_name="output.txt", output_path="./xwords/outputs/", intent_string=None,
               for_story=False):
    """
    Summary
    ----------
    Writes sentences into a .md file with the proper syntax

    Parameters
    ----------
    sentences:
        list of generated sentences to be written in the file
    file_name:
        name (string) of the file to be written
    output_path: 
        path (string) to the folder where to write file
    intent_string:
        string specifying the intent of sentences in the case of 
        Rasa NLU training file
    for_story:
        if True, writes output using Rasa Core's training format
        if False, writes output using Rasa NLU's training format

    Returns
    -------
        None

    """

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    full_path = output_path + file_name

    with open(full_path, mode='w') as output_file:
        if not for_story and intent_string is not None:
            output_file.write("## intent:" + intent_string + "\n")
        for s in sentences:
            # using Rasa Core (conversations) or Rasa NLU (only sentences)
            # training format
            if for_story:
                output_file.write(s + "\n")
            else:
                output_file.write("- " + s + "\n")

        print(len(sentences), "objects written in file", full_path)


def write_sentences(sentences, output_path="./xwords/outputs/", intent_string=None, 
                    output_prefix='', training_ratio=1.0, for_story=False):
    """
    Summary
    ----------
    Writes sentences into a .md file with the proper syntax

    Parameters
    ----------
    sentences:
        list of generated sentences to be written into a flat text file
    intent_string:
        string specifying the intent of sentences in the case of 
        Rasa NLU training file
    training_ratio:
        percentage of sentences/conversations to be kept separate in a test set
    output_path:
        path to the desired location for generated files
    for_story:
        if True, writes output using Rasa Core's training format
        if False, writes output using Rasa NLU's training format

    Returns
    -------
        None.
        Writes the number of sentences in the created training and testing sets
        files

    """

    nb_sentences = len(sentences)
    # select a subsample of sentences and split into training and testing set
    sub_samp = sorted(random.sample(range(nb_sentences),
                      int(nb_sentences*training_ratio)))
    training_sentences = [sentences[k] for k in sub_samp]

    # outputing into 'training.md' if no prefix is given
    file_name = output_prefix + "training.md"
    write_file(training_sentences, file_name, output_path, intent_string, for_story)

    if training_ratio != 1.0:
        # case of split between training and testing set
        traintest_sep = sorted(list(set(range(nb_sentences)) - set(sub_samp)))
        testing_sentences = [sentences[k] for k in traintest_sep]
        # outputing into 'test.md' if no prefix is given
        file_name_test = output_prefix + "testing.md"
        write_file(testing_sentences, file_name_test,
                   output_path, intent_string, for_story)


def generate(input_path, output_path="./xwords/outputs/", intent_string=None, output_prefix='',
             training_ratio=1.0, for_story=False, n_sub=None):
    """
    Summary
    ----------
    Generates train and test files for Rasa NLU/Core from config file

    Parameters
    ----------
    input_path:
        path to config file
    output_path:
        path to the desired location for generated files
    intent_string:
        string specifying the intent of sentences in the case of 
        Rasa NLU training file
    training_ratio:
        percentage of sentences/conversations to be kept separate in a test set
     for_story:
        if True, writes output using Rasa Core's training format
        if False, writes output using Rasa NLU's training format
    n_sub:
        number of randomly selected sentences or created stories to subsample 
        from the total number of combinations. If None, returns the full set of 
        sentence combinations (only possible when for_story=False).       


    Returns
    -------
        None.
        Writes the number of sentences in the created training and testing sets
        files

    """

    lines = parse_input(input_path)
    intents_list, entities_dic, aliases_dic = populate_entry_dicts(lines)

    if for_story:
        output = generate_stories(intent_string, entities_dic, n_sub)
    else:
        output = generate_sentences(intents_list, entities_dic, aliases_dic,
                                    n_sub)
    write_sentences(output, output_path, intent_string,
                    output_prefix, training_ratio, for_story)


