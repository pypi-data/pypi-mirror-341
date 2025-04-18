import click

import json
import sys
from urllib.parse import urlparse, urlunparse, urlencode
from urllib.request import urlopen, URLError, HTTPError

from .common import getjson, loadpadinfo


@click.command("call listAllPads and print the results")
@click.option("--padinfo", default="etherpad_info.json", help="settings, default: etherpad_info.json")
@click.option("--showurl/--noshowurl", default=False)
@click.option("--format", default="lines", help="output format: lines, json; default lines")
def main (padinfo, showurl, format):
    info = loadpadinfo(padinfo)
    if not info:
        sys.exit(0)

    apiurl =  info.get("apiurl")
    # apiurl = {0[protocol]}://{0[hostname]}:{0[port]}{0[apiurl]}{0[apiversion]}/".format(info)
    data = {}
    data['apikey'] = info['apikey']
    requesturl = apiurl+'listAllPads?'+urlencode(data)
    if showurl:
        print (requesturl)
    else:
        results = getjson(requesturl)['data']['padIDs']
        if format == "json":
            print (json.dumps(results))
        else:
            for r in results:
                print (r)

