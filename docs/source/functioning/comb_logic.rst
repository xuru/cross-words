Combination logic
==================================

cross-words is designed to compute sentences by placing all entities and alias alternative into all intents.

As a rule of thumb, the overall maximum number of generated sentences is in the order of:

nbintent sentences × avg. nbentity placeholders per intent sentence × avg. nbalternatives per entity × avg. nbalias placeholders per intent sentence × avg. nbalternatives per alias

As such, the created training files grow exponentially, hence the available n_sub parameter in generate

In the specific case of stories (Rasa Core), cross-words will also use information availability as an additional combination dimension.

For example, the two stories below are based on a different initially available information set given by the user:

.. code-block:: json

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