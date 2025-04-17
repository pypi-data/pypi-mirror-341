16 Sep 2021
------------

* translation of existing decisions into options (__SEMANTICSECTIONS__)
* __MULTI__ to trigger custom multilang (markdown) preprocess filter
* "regular" usage with __NOPUBLISH__ (resulting in accessRights rdfa in output HTML)
* new options (__TOC__)
* magic words for media publishing, copy indexalist templates in generic pad+etherdump version (__TAGS__ (default on) and __TYPES__ ?? or __VIDEO__ ... do we need item level words ? __SEMANTICPARAGRAPHS__)
* Magic words for (item) licenses?
* Remake the Sconstruct + allow centralized -- in db sconstruct per media folder.
* Redeploy using sponge user ipv constant

So in the makefile/sconstruct, the ultimate pandoc command was in the form:

```bash
    pandoc \
        --to markdown+lists_without_preceding_blankline+hard_line_breaks-space_in_atx_header
        --to html5+smart \
        --standalone \
        --section-divs \
        --css lib/wefts.css \
        -V lastmodified=(extract meta for lastmodified)
        --template TEMPLATE
```

So it's a mix of pandoc no arg options (standalone, section-divs), opts with args (-css, -V, --template) and the format options --to + --from.

For CSS: how to allow another pad to contain CSS? (tricky, needs to trigger etherdump to pull this source as well)

markdown (from) opts

* lists_without_preceding_blankline = +lists_without_preceding_blankline
* hard_line_breaks = +hard_link_breaks
* NO_space_in_atx_header = -space_in_atx_header

html5 (to) opts

* +smart

standalone opts

* __STANDALONE__
* __SECTION_DIVS__


etherdump preprocess:
* input: etherpad
* output: .md + .meta + build.sh


test.markdown test.magic.json: test (feed)
    etherdump preprocess --magic test.magic.json > test.markdown

test.sh: test.magic.json
    etherdump template 

test.html: test.sh
    bash test.sh