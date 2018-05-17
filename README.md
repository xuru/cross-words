cross-words
==========================================

`cross-words` is a python module that allows you to easily create a corpus of documents with parameterized entities.  

The main goal of `cross-words` is to offer an easy way to create either sentences or stories for use in chat bot training.
As of May 2018, it is mostly designed to be used with [Rasa NLU/Core](http://rasa.com/)

1. [Installation](#install)
2. [How to use this package](#usage)

# 1. Installation<a name="install"></a>

You can install it with pip:

    pip install cross-words

Or directly from github if you want the latest development version

    pip install git+https://github.com/data-chirps/cross-words.git

# 2. How to use this package<a name="usage"></a>
## cross-words DSL
`cross-words` is based on a simple yet powerful Domain Specific Language.
When used along with Rasa NLU/Core, it uses 3 concepts:

- **intents:** the objective of the chatbot's user (e.g. ask to book a restaurant, confirm a chatbot inquiry etc.)
- **entities:** specific parts of a sentence containing key information (e.g. which restaurant to book, how many people etc.)
- **aliases:** lists of synonyms that can be used interchangeably

More details are available at [Rasa NLU](https://nlu.rasa.com/tutorial.html)

Given a configuration file (.txt) containing all of the above, `cross-words` is able to generate many training sentences/conversations using combinations of sentence parts.

`cross-words` configuration files look like this:

```
Could I have the number of @[subject_filter] ~[owners] in @[geo_filter] @[time_filter]?


@[time_filter]
    this month
    this year
    LTD
        life to date
        up to date
    since release
        since launch
    since beginning of fiscal year

@[geo_filter]
    France
    Germany
    US
        United States
        America
    Canada
    Italy

@[subject_filter]
    birds
        parrots
        owl
    dogs
    cats
        persian


~[owners]
    owners
    possessors
```

If asked for sentences, `cross-words` will generate a .md file whose first lines will be :

```
- Could I have the number of [birds](subject_filter) possessors in [Canada](geo_filter) [life to date](time_filter)?
- Could I have the number of [parrots](subject_filter) possessors in [United States](geo_filter) [since release](time_filter)?
- Could I have the number of [owl](subject_filter) possessors in [Italy](geo_filter) [up to date](time_filter)?
- Could I have the number of [owl](subject_filter) possessors in [Italy](geo_filter) [since release](time_filter)?
- Could I have the number of [dogs](subject_filter) owners in [United States](geo_filter) [LTD](time_filter)?
- Could I have the number of [dogs](subject_filter) owners in [Canada](geo_filter) [this year](time_filter)?
- Could I have the number of [cats](subject_filter) owners in [France](geo_filter) [this year](time_filter)?
- Could I have the number of [cats](subject_filter) owners in [US](geo_filter) [since release](time_filter)?
- Could I have the number of [cats](subject_filter) owners in [America](geo_filter) [this month](time_filter)?
- Could I have the number of [cats](subject_filter) owners in [Canada](geo_filter) [life to date](time_filter)?

```
This file is then ready to use as training input to Rasa NLU.

If asked for stories:

```
## Genereated Story 815310784239368
* acquisition{}
    - utter_ask_time_filter
* acquisition{"time_filter": "since beginning of fiscal year"}
    - slot{"time_filter": "since beginning of fiscal year"}
    - utter_ask_geo_filter
* acquisition{"geo_filter": "America"}
    - slot{"geo_filter": "America"}
    - utter_ask_subject_filter
* acquisition{"subject_filter": "dogs"}
    - slot{"subject_filter": "dogs"}
    - action_acquisition

## Genereated Story 257661587723758
* acquisition{"time_filter": "since release", "geo_filter": "Germany"}
    - slot{"time_filter": "since release"}
    - slot{"geo_filter": "Germany"}
    - utter_ask_subject_filter
* acquisition{"subject_filter": "owl"}
    - slot{"subject_filter": "owl"}
    - action_acquisition

## Genereated Story 877699493192194
* acquisition{"subject_filter": "parrots"}
    - slot{"subject_filter": "parrots"}
    - utter_ask_time_filter
* acquisition{"time_filter": "LTD"}
    - slot{"time_filter": "LTD"}
    - utter_ask_geo_filter
* acquisition{"geo_filter": "France"}
    - slot{"geo_filter": "France"}
    - action_acquisition
```
This file is then ready to use for training with Rasa Core.

## Generating files

`cross-words` mainly comes with 2 functions: parse_input and generate. All other functions are implementation details.

### generate(input_path, output_path="./xwords/outputs/", intent_string=None, training_ratio=1.0, n_sub=None, for_story=False)
This is the main function of `cross-words'.

Given an input configuration file, it outputs all combinations of intents x entities x aliases into a .md file ready for training.

A few arguments allow to tune its behavior:

- **input_path:** path to the configuration file *(string)*
- **output_path:** path to the output folder where train/test files will be written *(string)*
- **intent_string** string to specify intent at the beginning of sentence files (for Rasa NLU) or inside genereated stories (for Rasa Core)
- **training_ratio:** ratio between train and test sets. If .7, 30% of all generated combinations will be reserved into a test file. If 1.0, no test file will be created. *(float)*
- **n_sub:** number of sentences/stories (incl. test) to be taken as a subsample of all possible combinations of intents x entities x aliases *(int)* (required when generating stories for Rasa Core)
- **for_story:** whether to generate sentences (for Rasa NLU) or stories (for Rasa Core) *(bool)*

### parse_input(input_path)
This function is provided as a facilitator for experimentation purposes. It is the first function called by generate.

Given an input configuration file, generates:

- a list of intents in the form
```
    ['intent_sentence_0', 'intent_sentence_1', ...]

    e.g. from above:
    ['Could I have the number of @[subject_filter] ~[owners] in @[geo_filter] @[time_filter]?']
```
- a dictionnary of entitites in the form
```
    {'entity_0': ['alternative_00', 'alternative_01', ...],
     'entity_1': ['alternative_10', 'alternative_11', ...], ...}

    e.g. from above:
    {'time_filter': ['this month', 'this year', ...],
     'geo_filter': ['France', 'Germany', ...], ...}
```
- a dictionnary of synonyms in the form
```
    {'alias_0': ['alternative_00', 'alternative_01', ...],
     'alias_1': ['alternative_10', 'alternative_11', ...], ...}

    e.g. from above:
    {'owners': ['owners', 'possessors']}
```

## Combination logic

`cross-words` is designed to compute sentences by placing all entities and alias alternative into all intents.

As a rule of thumb, the overall maximum number of generated sentences is in the order of:

nb<sub>intent sentences</sub> &times; avg. nb<sub>entity placeholders per intent sentence</sub> &times; avg. nb<sub>alternatives per entity</sub> &times; avg. nb<sub>alias placeholders per intent sentence</sub> &times; avg. nb<sub>alternatives per alias</sub>

As such, the created training files grow exponentially, hence the available *n_sub* parameter in **generate**

In the specific case of stories (Rasa Core), `cross-words` will also use *information availability* as an additional combination dimension.

For example, the two stories below are based on a different initially available information set given by the user:

```
## Genereated Story 257661587723758
* acquisition{"time_filter": "since release", "geo_filter": "Germany"}
    - slot{"time_filter": "since release"}
    - slot{"geo_filter": "Germany"}
    - utter_ask_subject_filter
* acquisition{"subject_filter": "owl"}
    - slot{"subject_filter": "owl"}
    - action_acquisition

## Genereated Story 877699493192194
* acquisition{"time_filter": "since release"}
    - slot{"time_filter": "since release"}
    - utter_ask_subject_filter
* acquisition{"subject_filter": "owl"}
    - slot{"subject_filter": "owl"}
    - utter_ask_geo_filter
* acquisition{"geo_filter": "Germany"}
    - slot{"geo_filter": "Germany"}
    - action_acquisition 
```