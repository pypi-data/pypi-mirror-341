etherdump
=========

Tool to help manage periodic publishing of [etherpads](http://etherpad.org/) to static files, preserving metadata. Uses the etherpad API (and so it requires having the APIKEY.txt contents of an etherpad installation).


Installation
-------------

    pip install etherdump

Usage
---------------
	mkdir mydump
	cd myddump
	etherdump init

The settings are placed in a file called etherpad_info.json (by default) and can be specified with the --padinfo option on subcommands. **Make sure that this file is not exposed publically, as it contains the APIKEY to the etherpad server.**

	etherdump list

You should see a list of pads.



Cookbook
========================

Using etherdump to maintain a static HTML archive of pads
-------------------------------------------------------------------

	# Mis à jour les pads changé
	etherdump pull --padinfo ..path/to/etherpad_info.json

	# Récrée les pages index...
	etherdump index --padinfo ../path/to/etherpad_info.json


Using etherdump to migrate from one etherpad instance to another
------------------------------------------------------------------

    mkdir instance1 && cd instance1
    etherdump init
    etherdump pull

    (cd ..)
    mkdir instance2 && cd instance2
    etherdump init
    etherdump pushhtml --basepath ../instance1 ../instance1/p/*.meta.json

NB: sethtml/pushhtml seems to only work on the server itself, ie using API url such as localhost:9001.

NB: This command indescriminantly clobbers pads in instance2 with the HTML of the dumped versions from instance1.

This technique can be used to "reset" the database of a pad by recreating pads (without their history or editor info/colors) in a fresh database.



