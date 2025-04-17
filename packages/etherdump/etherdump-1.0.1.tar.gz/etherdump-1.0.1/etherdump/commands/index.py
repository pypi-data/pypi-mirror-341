# from argparse import ArgumentParser

"""
goal: simplify so that index meta data is already formatted for the index.... ?!
(why isn't this already the case)

"""


import sys, json, re, os, time
from datetime import datetime
from time import sleep
from urllib.parse import urlparse, urlunparse, urlencode, quote
from urllib.request import urlopen, URLError, HTTPError
from pathlib import Path
from shutil import copyfile
from xml.etree import ElementTree as ET

import click
import dateutil.parser
from jinja2 import FileSystemLoader, Environment
import html5lib

from etherdump.commands.common import *
from .html5tidy import tree_sub_hrefs


"""
index:
    Generate pages from etherdumps using a template.

    Built-in templates: rss.xml, index.html

"""

def group (items, key=lambda x: x):
    """ returns a list of lists, of items grouped by a key function """
    ret = []
    keys = {}
    for item in items:
        k = key(item)
        if k not in keys:
            keys[k] = []
        keys[k].append(item)
    for k in sorted(keys):
        keys[k].sort()
        ret.append(keys[k])
    return ret

# def base (x):
#     return re.sub(r"(\.raw\.html)|(\.diff\.html)|(\.meta\.json)|(\.raw\.txt)$", "", x)

def splitextlong (x):
    """ split "long" extensions, i.e. foo.bar.baz => ('foo', '.bar.baz') """
    m = re.search(r"^(.*?)(\..*)$", x)
    if m:
        return m.groups()
    else:
        return x, ''

def base (x):
    return splitextlong(x)[0]

def excerpt (t, chars=25):
    if len(t) > chars:
        t = t[:chars] + "..."
    return t

def absurl (url, base=None):
    if not url.startswith("http"):
        return base + url
    return url

def url_base (url):
    (scheme, netloc, path, params, query, fragment) = urlparse(url)
    path, _ = os.path.split(path.lstrip("/"))
    ret = urlunparse((scheme, netloc, path, None, None, None))
    if ret:
        ret += "/"
    return ret

def datetimeformat (t, format='%Y-%m-%d %H:%M:%S'):
    if type(t) == str:
        dt = dateutil.parser.parse(t)
        return dt.strftime(format)
    else:
        return time.strftime(format, time.localtime(t))

@click.command(help="Convert dumped files to a document via a template.")
@click.argument("input", nargs=-1)
@click.option("--templatepath", help="path to find templates, default: built-in")
@click.option("--template", default="index.html", show_default=True)
@click.option("--padinfo", default="etherpad_info.json", show_default=True)
@click.option("--order", default="padid", type=click.Choice(("padid", "pad", "lastedited", "authors", "revisions"), case_sensitive=False), show_default=True)
@click.option("--reverse/--not-reversed", default=False, show_default=True)
@click.option("--limit", type=int, default=0, help="limit, 0 means no limit", show_default=True)
@click.option("--skip", type=int, default=0, show_default=True)
# @click.option("--rss-full-content/--rss-excerpt", default=False, help="Include full content in RSS feed", show_default=True)
@click.option("--link", default="diffhtml,html,text", help="link variable will be to this version, can be comma-delim list, use first avail, default: diffhtml,html,text")
@click.option("--linkbase", default="", help="base url to use for links, default: try to use the feedurl")
@click.option("--output", type=click.Path(), default="index.html")
@click.option("--title", default="etherdump", show_default=True)
@click.option("--language", show_default=True)
@click.option("--timestamp", default=None, help="timestamp, default: now (e.g. 2015-12-01 12:30:00)")
@click.option("--set", nargs=2, multiple=True, help="set variables in the template")
def main (input, templatepath, template, padinfo, order, reverse, limit, skip, link, linkbase, output, title, language, timestamp, set):
    # p = ArgumentParser("Convert dumped files to a document via a template.")

    # p.add_argument("input", nargs="+", help="Files to list (.meta.json files)")

    # p.add_argument("--templatepath", default=None, help="path to find templates, default: built-in")
    # p.add_argument("--template", default="index.html", help="template name, built-ins include index.html, rss.xml; default: index.html")
    # p.add_argument("--padinfo", default="etherpad_info.json", help="settings, default: etherpad_info.json")
    # # p.add_argument("--zerorevs", default=False, action="store_true", help="include pads with zero revisions, default: False (i.e. pads with no revisions are skipped)")

    # p.add_argument("--order", default="padid", help="order, possible values: padid, pad (no group name), lastedited, (number of) authors, revisions, default: padid")
    # p.add_argument("--reverse", default=False, action="store_true", help="reverse order, default: False (reverse chrono)")
    # p.add_argument("--limit", type=int, default=0, help="limit to number of items, default: 0 (no limit)")
    # p.add_argument("--skip", default=None, type=int, help="skip this many items, default: None")

    # p.add_argument("--content", default=False, action="store_true", help="rss: include (full) content tag, default: False")
    # p.add_argument("--link", default="diffhtml,html,text", help="link variable will be to this version, can be comma-delim list, use first avail, default: diffhtml,html,text")
    # p.add_argument("--linkbase", default=None, help="base url to use for links, default: try to use the feedurl")
    # p.add_argument("--output", default=None, help="output, default: stdout")

    # p.add_argument("--files", default=False, action="store_true", help="include files (experimental)")

    # pg = p.add_argument_group('template variables')
    # pg.add_argument("--feedurl", default="feed.xml", help="rss: to use as feeds own (self) link, default: feed.xml")
    # pg.add_argument("--siteurl", default=None, help="rss: to use as channel's site link, default: the etherpad url")
    # pg.add_argument("--title", default="etherdump", help="title for document or rss feed channel title, default: etherdump")
    # pg.add_argument("--description", default="", help="rss: channel description, default: empty")
    # pg.add_argument("--language", default="en-US", help="rss: feed language, default: en-US")
    # pg.add_argument("--updatePeriod", default="daily", help="rss: updatePeriod, possible values: hourly, daily, weekly, monthly, yearly; default: daily")
    # pg.add_argument("--updateFrequency", default=1, type=int, help="rss: update frequency within the update period (where 2 would mean twice per period); default: 1")
    # pg.add_argument("--generator", default="https://gitlab.com/activearchives/etherdump", help="generator, default: https://gitlab.com/activearchives/etherdump")
    # pg.add_argument("--timestamp", default=None, help="timestamp, default: now (e.g. 2015-12-01 12:30:00)")
    # pg.add_argument("--next", default=None, help="next link, default: None)")
    # pg.add_argument("--prev", default=None, help="prev link, default: None")

    # args = p.parse_args(args)
    
    tmpath = templatepath
    # Default path for template is the built-in data/templates
    if tmpath == None:
        tmpath = os.path.split(os.path.abspath(__file__))[0]
        tmpath = os.path.split(tmpath)[0]
        tmpath = os.path.join(tmpath, "data", "templates")

    env = Environment(loader=FileSystemLoader(tmpath))
    env.filters["excerpt"] = excerpt
    env.filters["datetimeformat"] = datetimeformat
    template_path = template
    template = env.get_template(template)

    info = loadpadinfo(padinfo)
    if not info:
        return

    inputs = list(input)
    inputs.sort()
    # Use "base" to strip (longest) extensions
    # inputs = group(inputs, base)

    def wrappath (p):
        path = "./{0}".format(p)
        ext = os.path.splitext(p)[1][1:]
        return {
            "url": path,
            "path": path,
            "code": 200,
            "type": ext
        }

    def metaforpaths (paths):
        ret = {}
        pid = base(paths[0])
        ret['pad'] = ret['padid'] = pid
        ret['versions'] = [wrappath(x) for x in paths]
        lastedited = None
        for p in paths:
            mtime = os.stat(p).st_mtime 
            if lastedited == None or mtime > lastedited:
                lastedited = mtime
        ret["lastedited_iso"] = datetime.fromtimestamp(lastedited).strftime("%Y-%m-%dT%H:%M:%S")
        ret["lastedited_raw"] = mtime 
        return ret

    def loadmeta(p):
        # Consider a set of grouped files
        # Otherwise, create a "dummy" one that wraps all the files as versions
        if p.endswith(".meta.json"):
            with open(p) as f:
                return json.load(f)
        # # IF there is a .meta.json, load it & MERGE with other files
        # if ret:
        #     # TODO: merge with other files
        #     for p in paths:
        #         if "./"+p not in ret['versions']:
        #             ret['versions'].append(wrappath(p))
        #     return ret
        # else:
        #     return metaforpaths(paths)

    def fixdates (padmeta):
        d = dateutil.parser.parse(padmeta["lastedited_iso"])
        padmeta["lastedited"] = d
        padmeta["lastedited_822"] = d.strftime("%a, %d %b %Y %H:%M:%S +0000")
        return padmeta

    pads = map(loadmeta, inputs)
    pads = [x for x in pads if x != None]
    pads = map(fixdates, pads)
    pads = list(pads)

    def could_have_base (x, y):
        return x == y or (x.startswith(y) and x[len(y):].startswith("."))

    def get_best_pad (x):
        for pb in padbases:
            p = pads_by_base[pb]
            if could_have_base(x, pb):
                return p

    def has_version (padinfo, path):
        return [x for x in padinfo['versions'] if 'path' in x and x['path'] == "./"+path]

    # if args.files:
    #     inputs = input
    #     inputs.sort()
    #     removelist = []

    #     pads_by_base = {}
    #     for p in pads:
    #         # print ("Trying padid", p['padid'], file=sys.stderr)
    #         padbase = os.path.splitext(p['padid'])[0]
    #         pads_by_base[padbase] = p
    #     padbases = list(pads_by_base.keys())
    #     # SORT THEM LONGEST FIRST TO ensure that LONGEST MATCHES MATCH
    #     padbases.sort(key=lambda x: len(x), reverse=True)
    #     # print ("PADBASES", file=sys.stderr)
    #     # for pb in padbases:
    #     #     print ("  ", pb, file=sys.stderr)
    #     print ("pairing input files with pads", file=sys.stderr)
    #     for x in inputs:
    #         # pair input with a pad if possible
    #         xbasename = os.path.basename(x)
    #         p = get_best_pad(xbasename)
    #         if p:
    #             if not has_version(p, x):
    #                 print ("Grouping file {0} with pad {1}".format(x, p['padid']), file=sys.stderr)
    #                 p['versions'].append(wrappath(x)) 
    #             else:
    #                  print ("Skipping existing version {0} ({1})...".format(x, p['padid']), file=sys.stderr)
    #             removelist.append(x)
    #     # Removed Matches files
    #     for x in removelist:
    #         inputs.remove(x)
    #     print ("Remaining files:", file=sys.stderr)
    #     for x in inputs:
    #          print (x, file=sys.stderr)
    #     print (file=sys.stderr)
    #     # Add "fake" pads for remaining files
    #     for x in inputs:
    #         pads.append(metaforpaths([x]))

    if timestamp is None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    padurlbase = re.sub(r"api/1.2.9/$", "p/", info["apiurl"])
    # if type(padurlbase) == unicode:
    #     padurlbase = padurlbase.encode("utf-8")
    siteurl = padurlbase
    utcnow = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S +0000")

    # order items & apply limit
    if order == "lastedited":
        pads.sort(key=lambda x: x.get("lastedited_iso"), reverse=reverse)
    elif order == "pad":
        pads.sort(key=lambda x: x.get("pad"), reverse=reverse)
    elif order == "padid":
        pads.sort(key=lambda x: x.get("padid"), reverse=reverse)
    elif order == "revisions":
        pads.sort(key=lambda x: x.get("revisions"), reverse=reverse)
    elif order == "authors":
        pads.sort(key=lambda x: len(x.get("authors")), reverse=reverse)
    else:
        raise Exception("That ordering is not implemented!")

    if limit:
        pads = pads[:limit]

    linkversions = link.split(",")
    # linkbase = linkbase or url_base(feedurl)

    for p in pads:
        versions_by_type = {}
        p["versions_by_type"] = versions_by_type
        for v in p["versions"]:
            t = v["type"]
            versions_by_type[t] = v

        if "text" in versions_by_type:
            try:
                with open (versions_by_type["text"]["path"], errors="replace") as f:
                    p["text"] = f.read()
            except FileNotFoundError:
                p['text'] = ''
        # ADD IN LINK TO PAD AS "link"
        for v in linkversions:
            if v in versions_by_type:
                vdata = versions_by_type[v]
                try:
                    if v == "pad" or os.path.exists(vdata["path"]):
                        p["link"] = absurl(vdata["url"], linkbase)
                        break
                except KeyError as e:
                    pass
    tvars = {}
    tvars['pads'] = pads
    tvars['title'] = title
    tvars['order'] = order
    tvars['limit'] = limit
    tvars['skip'] = skip
    tvars['timestamp'] = timestamp
    for name, value in set:
        tvars[name] = value
    
    src = template.render(**tvars)

    if template_path.endswith(".html"):
        doc = html5lib.parse(src, treebuilder="etree", namespaceHTMLElements=False)
        # html5tidy(doc, indent=True, title=padid, scripts=script, links=links, viewport_meta="width=device-width,initial-scale=1")
        files_to_copy = []
        def static_sub (m):
            filename = m.group(1)
            files_to_copy.append(filename)
            return "static/"+m.group(1)
        tree_sub_hrefs(doc, r"^/static/(.*)$", static_sub)
        # ensure files_to_copy
        output_parent = Path(output).parent
        output_parent.mkdir(exist_ok=True)
        output_static = output_parent / "static"
        output_static.mkdir(exist_ok=True)
        static_path = Path(__file__).parent.parent / "data" / "templates" / "static"
        for file in files_to_copy:
            output_file = output_static / file
            if not output_file.exists():
                copyfile(static_path / file, output_file)
        src = ET.tostring(doc, method="html", encoding="unicode")

    with open (output, "wt") as fout:
        print(src, file=fout)


