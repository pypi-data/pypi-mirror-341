CHANGE LOG
================

Originally designed for use at [constant](http://etherdump.constantvzw.org/).


17 Oct 2016
-----------------------------------------------
Preparations for [Machine Research](https://machineresearch.wordpress.com/) [2](http://constantvzw.org/site/Machine-Research,2646.html)


6 Oct 2017
----------------------
Feature request from PW: When deleting a previously public document, generate a page / pages with an explanation (along the lines of "This document was previously public but has been marked .... maybe give links to search").

3 Nov 2017
---------------
machineresearch seems to be \_\_NOPUBLISH__ but still exists (also in recentchanges)

Jan 2018
-------------
Updated files to work with python3 (probably this has broken python2).

Jun 2019
-------------
Revised sethtml & added pushhtml

Sep 2021
-----------
Adding/updating general purpose magicwords


2022 02 11
----------------

2022 Revisiting etherdump code to really consider what's used and deprecate useless / questionable subcommands.
ALSO in order to add new commands for pre/post processing + magic words...

Does it makes sense to use scons internally?


### tested / useful

* list
* listauthors
* deletepad
* pull
* index
* init
* pushhtml
* sethtml
* settext
* revisionscount (sub behaviour of showmeta?)
* gettext
* status OK it's there to work like git, but is it used?
* dumpcsv
* template
* html5tidy
* preprocess


### deprecate?

* showmeta: only opens a .meta.json file from padid, rather lame and misleading -- or improve it!?
* join
* appendmeta

variations on pull?
	creatediffhtml
	gethtml

### magicwords

How to do in a *porous* way... ie could magicwords by (python/bash) scripts!
And how could they (best) be defineable external to etherdump...

Dynamic import.. but would be cool to have a mix of built in (basis) behavious like {{NOPUBLISH}}


April 2025
--------------
Bumping version to 1.0.0 and updating project to *hopefully* properly package and publish. Using uv and hatchling. Removing bin/etherdump in favor of locating this in etherdump.main. Removing python2 code.

Updating init command to remove (flawed!) default assumption that making an .etherdump/settings.json by default is a good idea. In practice it obscures that private information (an etherpad APIKEY) could be made inadvertantly public. New value is "etherpad_info.json". Already have added explicit --padinfo option to the commands, changing default value to be etherpad_info.json.

Add/update index templates!

Noticing that gettext uses the "new" Etherpad class... but not other functions. This is odd and shows an incomplete possible migration to code based on a class embedding different API calls directly.

TODO: Test template command, installing necessary deps, 

DOCUMENT COMMON USAGE (a la sync.sh on constant's etherdump).

ALSO: Trying to add support for etherpads new default style [SSO authentication](https://docs.etherpad.org/api/http_api.html#authentication).

12 April 2025
---------------
* version 1.0.1
* want to remove use of cdn in index template, also opportunity to improve the default stying



