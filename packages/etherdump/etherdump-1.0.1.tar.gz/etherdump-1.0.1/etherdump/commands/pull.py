# from argparse import ArgumentParser
import click
import sys, json, re, os
from datetime import datetime
from urllib.parse import urlencode, quote
from urllib.request import urlopen, URLError, HTTPError

from etherdump.etherpad import Etherpad
from etherdump.commands.common import *
from time import sleep
from etherdump.commands.html5tidy import html5tidy
import html5lib
from xml.etree import ElementTree as ET
from fnmatch import fnmatch

from .common import loadpadinfo

# debugging
# import ElementTree as ET 

"""
pull(meta):
    Update meta data files for those that have changed.
    Check for changed pads by looking at revisions & comparing to existing


todo...
use/prefer public interfaces ? (export functions)


"""

@click.command(name="etherdump pull", help="Check for pads that have changed since last sync (according to .meta.json)")
@click.argument("padid", nargs=-1)
@click.option("--glob", help="download pads matching a glob pattern")
@click.option("--padinfo", default="etherpad_info.json", show_default=True)
@click.option("--zerorevs/--no-zerorevs", default=False, help="include pads with zero revisions", show_default=True)
@click.option("--pub", default=".", help="folder to store files for public pads", show_default=True)
@click.option("--group", default="g", help="folder to store files for group pads", show_default=True)
@click.option("--skip", default=0, type=int, help="skip this many items", show_default=True)
@click.option("--meta/--no-meta", default=True, help="download meta to PADID.meta.json", show_default=True)
@click.option("--text/--no-text", default=True, help="download text to PADID.txt", show_default=True)
@click.option("--html/--no-html", default=True, help="download html to PADID.html", show_default=True)
@click.option("--dhtml/--no-dhtml", default=False, help="use the API to compute a dhtml and save to PADID.diff.html", show_default=True)
@click.option("--etherpad/--no-etherpad", default=False, help="download etherpad history to PADID.etherpad.json", show_default=True)
@click.option("--folder/--no-folder", default=False, help="download etherpad versions to a folder named PADID", show_default=True)
@click.option("--output/--no-output", default=False, help="output names of changed padids", show_default=True)
@click.option("--force/--no-force", default=False, help="reload, even if revisions count matches previous", show_default=True)
@click.option("--no-raw-ext/--raw-ext", default=False, help="save pad text with no (additional) extension (good when pad names themselves have extensions)", show_default=True)
@click.option("--fix-names/--no-fix-names", default=False, help="normalize padid's (no spaces, special control chars) for use in file names", show_default=True)
@click.option("--css", default="styles.css", help="add css url to output pages", show_default=True)
@click.option("--script", default="script.js", help="add script url to output pages", show_default=True)
@click.option("--nopublish", default="__NOPUBLISH__", help="no publish magic word", show_default=True)
def main (padid, glob, padinfo, zerorevs, pub, group, skip, \
    meta, text, html, dhtml, etherpad, \
    folder, output, force, no_raw_ext, fix_names, css, script, nopublish):
    # p = ArgumentParser("Check for pads that have changed since last sync (according to .meta.json)")

    # p.add_argument("padid", nargs="*", default=[])
    # p.add_argument("--glob", default=False, help="download pads matching a glob pattern")

    # p.add_argument("--padinfo", default="etherpad_info.json", help="settings, default: etherpad_info.json")
    # p.add_argument("--zerorevs", default=False, action="store_true", help="include pads with zero revisions, default: False (i.e. pads with no revisions are skipped)")
    # p.add_argument("--pub", default="p", help="folder to store files for public pads, default: p")
    # p.add_argument("--group", default="g", help="folder to store files for group pads, default: g")
    # p.add_argument("--skip", default=None, type=int, help="skip this many items, default: None")
    # p.add_argument("--meta", default=False, action="store_true", help="download meta to PADID.meta.json, default: False")
    # p.add_argument("--text", default=False, action="store_true", help="download text to PADID.txt, default: False")
    # p.add_argument("--html", default=False, action="store_true", help="download html to PADID.html, default: False")
    # p.add_argument("--dhtml", default=False, action="store_true", help="download dhtml to PADID.diff.html, default: False")
    # p.add_argument("--all", default=False, action="store_true", help="download all files (meta, text, html, dhtml), default: False")
    # p.add_argument("--folder", default=False, action="store_true", help="dump files in a folder named PADID (meta, text, html, dhtml), default: False")
    # p.add_argument("--output", default=False, action="store_true", help="output changed padids on stdout")
    # p.add_argument("--force", default=False, action="store_true", help="reload, even if revisions count matches previous")
    # p.add_argument("--no-raw-ext", default=False, action="store_true", help="save plain text as padname with no (additional) extension")
    # p.add_argument("--fix-names", default=False, action="store_true", help="normalize padid's (no spaces, special control chars) for use in file names")

    # p.add_argument("--css", default="/styles.css", help="add css url to output pages, default: /styles.css")
    # p.add_argument("--script", default="/versions.js", help="add script url to output pages, default: /versions.js")

    # p.add_argument("--nopublish", default="__NOPUBLISH__", help="no publish magic word, default: __NOPUBLISH__")

    # args = p.parse_args(args)

    click.echo(f"etherdump version {VERSION}", err=True)

    info = loadpadinfo(padinfo)
    if not info:
        return
    # with open(args.padinfo) as f:
    #     info = json.load(f)
    ep = Etherpad(info.get("apiurl"), info.get("apikey"))

    raw_ext = ".raw.txt"
    if no_raw_ext:
        raw_ext = ""

    if padid:
        padids = padid
    else:
        padids = ep.list()
        if glob:
            padids = [x for x in padids if fnmatch(x, glob)]

    padids.sort()
    numpads = len(padids)
    # maxmsglen = 0
    count = 0

    if skip:
        padids = padids[skip:]

    with click.progressbar(padids) as padids_bar:
        for padid in padids_bar:
            click.echo(padid, err=True)
            # progressbar(i, numpads, padid)
            try:
                result = ep.pad_pull(\
                        padid=padid, \
                        pub=pub, \
                        group=group, \
                        fix_names=fix_names, \
                        folder=folder, \
                        zerorevs=zerorevs, \
                        meta=meta, \
                        text=text, \
                        html=html, \
                        dhtml=dhtml, \
                        nopublish=nopublish, \
                        output=output, \
                        css=css, \
                        script=script, \
                        force=force, \
                        raw_ext = raw_ext
                    )
                if result:
                    count += 1
            except Exception as ex:
                print(f"EXCEPTION {padid}: {ex}")

    click.echo(f"\n{count} pad(s) loaded", err=True)
