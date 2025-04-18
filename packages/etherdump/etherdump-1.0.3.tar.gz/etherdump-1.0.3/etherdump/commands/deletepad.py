from argparse import ArgumentParser
import json
from urllib.parse import urlencode
from urllib.request import urlopen, HTTPError, URLError
from .common import loadpadinfo

def main(args):
    p = ArgumentParser("calls the getText API function for the given padid")
    p.add_argument("padid", help="the padid")
    p.add_argument("--padinfo", default="etherpad_info.json", help="settings, default: etherpad_info.json")
    p.add_argument("--showurl", default=False, action="store_true")
    p.add_argument("--format", default="text", help="output format, can be: text, json; default: text")
    args = p.parse_args(args)

    info = loadpadinfo(args.padinfo)
    if not info:
        return
    apiurl = info.get("apiurl")
    # apiurl = "{0[protocol]}://{0[hostname]}:{0[port]}{0[apiurl]}{0[apiversion]}/".format(info)
    data = {}
    data['apikey'] = info['apikey']
    data['padID'] = args.padid # is utf-8 encoded
    requesturl = apiurl+'deletePad?'+urlencode(data)
    if args.showurl:
        print (requesturl)
    else:
        results = json.load(urlopen(requesturl))
        if args.format == "json":
            print (json.dumps(results))
        else:
            if results['data']:
                print (results['data']['text'].encode("utf-8"))
