from argparse import ArgumentParser
import json
from urllib.parse import urlencode
from urllib.request import urlopen, HTTPError, URLError
from .common import loadpadinfo


def main(args):
    p = ArgumentParser("call getRevisionsCount for the given padid")
    p.add_argument("padid", help="the padid")
    p.add_argument("--padinfo", default="etherpad_info.json", help="settings, default: etherpad_info.json")
    p.add_argument("--showurl", default=False, action="store_true")
    args = p.parse_args(args)

    info = loadpadinfo(args.padinfo)
    if not info:
        return
    apiurl = info.get("apiurl")
    data = {}
    data['apikey'] = info['apikey']
    data['padID'] = args.padid.encode("utf-8")
    requesturl = apiurl+'getRevisionsCount?'+urlencode(data)
    if args.showurl:
        print (requesturl)
    else:
        results = json.load(urlopen(requesturl))['data']['revisions']
        print (results)
