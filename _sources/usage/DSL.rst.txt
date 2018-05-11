cross-words' Domain Specific Language (DSL)
===========================================

cross-words is based on a simple yet powerful Domain Specific Language. When used along with Rasa NLU/Core, it uses 3 concepts:

intents: the objective of the chatbot's user (e.g. ask to book a restaurant, confirm a chatbot inquiry etc.)
entities: specific parts of a sentence containing key information (e.g. which restaurant to book, how many people etc.)
aliases: lists of synonyms that can be used interchangeably
More details are available at Rasa NLU

Given a configuration file (.txt) containing all of the above, cross-words is able to generate many training sentences/conversations using combinations of sentence parts.

cross-words configuration files look like this:

.. code-block:: yaml

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

If asked for sentences, cross-words will generate a .md file whose first lines will be:

.. code-block:: yaml

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

This file is then ready to use as training input to Rasa NLU.

If asked for stories:

.. code-block:: yaml

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

This file is then ready to use for training with Rasa Core.
