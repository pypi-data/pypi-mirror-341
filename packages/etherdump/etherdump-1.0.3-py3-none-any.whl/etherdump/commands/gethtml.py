from argparse import ArgumentParser
import json
from urllib.parse import urlencode
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from .common import loadpadinfo


def main(args):
    p = ArgumentParser("calls the getHTML API function for the given padid")
    p.add_argument("padid", help="the padid")
    p.add_argument("--padinfo", default="etherpad_info.json", help="settings, default: etherpad_info.json")
    p.add_argument("--showurl", default=False, action="store_true")
    p.add_argument("--format", default="text", help="output format, can be: text, json; default: text")
    p.add_argument("--rev", type=int, default=None, help="revision, default: latest")
    args = p.parse_args(args)

    info = loadpadinfo(args.padinfo)
    if not info:
        return
    apiurl = info.get("apiurl")
    # apiurl = "{0[protocol]}://{0[hostname]}:{0[port]}{0[apiurl]}{0[apiversion]}/".format(info)
    data = {}
    data['apikey'] = info['apikey']
    data['padID'] = args.padid
    if args.rev != None:
        data['rev'] = args.rev
    requesturl = apiurl+'getHTML?'+urlencode(data)
    if args.showurl:
        print (requesturl)
    else:
        results = json.loads(urlopen(requesturl).read().decode("utf-8"))['data']
        if args.format == "json":
            print (json.dumps(results))
        else:
            print (results['html'])
