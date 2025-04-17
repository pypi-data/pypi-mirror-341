import click

import re, os, json, sys
from math import ceil, floor
from time import sleep
from urllib.parse import urlparse, urlunparse, urlencode, quote_plus, unquote_plus
from urllib.request import urlopen, URLError, HTTPError
from html.entities import name2codepoint

VERSION = "1.0.0"

groupnamepat = re.compile(r"^g\.(\w+)\$")
def splitpadname (padid):
    m = groupnamepat.match(padid)
    if m:
        return(m.group(1), padid[m.end():])
    else:
        return (u"", padid)

def padurl (padid, ):
    return padid

def padpath (padid, pub_path=u"", group_path=u"", normalize=False):
    g, p = splitpadname(padid)
    # if type(g) == unicode:
    #     g = g.encode("utf-8")
    # if type(p) == unicode:
    #     p = p.encode("utf-8")
    p = quote_plus(p)
    if normalize:
        p = p.replace(" ", "_")
        p = p.replace("(", "")
        p = p.replace(")", "")
        p = p.replace("?", "")
        p = p.replace("'", "")
    if g:
        return os.path.join(group_path, g, p)
    else:
        return os.path.join(pub_path, p)

def padpath2id (path):
    if type(path) == unicode:
        path = path.encode("utf-8")
    dd, p = os.path.split(path)
    gname = dd.split("/")[-1]
    p = unquote_plus(p)
    if gname:
        return "{0}${1}".format(gname, p).decode("utf-8")
    else:
        return p.decode("utf-8")

def getjson (url, max_retry=3, retry_sleep_time=3):
    ret = {}
    ret["_retries"] = 0
    while ret["_retries"] <= max_retry:
        try:
            f = urlopen(url)
            data = f.read()
            data = data.decode("utf-8")
            rurl = f.geturl()
            f.close()
            ret.update(json.loads(data))
            ret["_code"] = f.getcode()
            if rurl != url:
                ret["_url"] = rurl
            return ret
        except ValueError as e:
            url = "http://localhost" + url
        except HTTPError as e:
            print ("HTTPError {0} {0}".format(url, e), file=sys.stderr)
            ret["_code"] = e.code
            ret["_retries"]+=1
            if retry_sleep_time:
                sleep(retry_sleep_time)
    return ret

def loadpadinfo(p):
    try:
        with open(p) as f:
            info = json.load(f)
            if 'localapiurl' not in info:
                info['localapiurl'] = info.get('apiurl')
        return info
    except FileNotFoundError as e:
        # click.echo(click.style('Hello World!', fg="green") + " PLAIN")
        click.echo(f"Could not load {click.style(p, bold=True)}")
        click.echo(f"Use {click.style('etherdump init', bold=True)} to create a settings file, then refer to it with the {click.style('--padinfo', bold=True)} option with subcommands.")
        return None

def progressbar (i, num, label="", file=sys.stderr):
    p = float(i) / num
    percentage = int(floor(p*100))
    bars = int(ceil(p*20))
    bar = ("*"*bars) + ("-"*(20-bars))
    msg = u"\r{0} {1}/{2} {3}... ".format(bar, (i+1), num, label)
    sys.stderr.write(msg)
    sys.stderr.flush()



# Python developer Fredrik Lundh (author of elementtree, among other things) has such a function on his website, which works with decimal, hex and named entities:
##
# Removes HTML or XML character references and entities from a text string.
#
# @param text The HTML (or XML) source text.
# @return The plain text, as a Unicode string, if necessary.
def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub(r"&#?\w+;", fixup, text)

