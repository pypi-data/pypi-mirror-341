from urllib.request import urlopen
from urllib.parse import urlencode
import json
import re
import argparse


def create_pad (apiurl, apikey, padid):
    # url = "http://{0}/api/1/createPad".format(hostport)
    url = apiurl + "createPad"
    data = (
        ('apikey', apikey),
        ('padID', padid),
    )
    f = urlopen(url, data=urlencode(data).encode("utf-8"))
    return json.loads(f.read().decode("utf-8"))


def sethtml (apiurl, apikey, padid, html):
    # strip the (initial) title tag
    html = re.sub(r"<title>.*?</title>", "", html, 1, re.I)
    data = (
        ('apikey', apikey),
        ('padID', padid),
        ('html', html)
    )
    # url = "http://{0}/api/1/setHTML".format(hostport)
    url = apiurl + "setHTML"
    data = urlencode(data).encode("utf-8")
    f = urlopen(url, data=data)
    return json.loads(f.read().decode("utf-8"))

def pushhtml (apiurl, apikey, padid, html):
    """ Use sethtml, call createPad if necessary """
    resp = sethtml(apiurl, apikey, padid, html)
    if resp['code'] == 1:
        # print ("ERROR {0}, trying to create pad first".format(resp['message']))
        create_pad(apiurl, apikey, padid)
        resp = sethtml(apiurl, apikey, padid, html)
    return resp


def main(args):
    p = argparse.ArgumentParser("calls the setHTML API function for the given padid")
    p.add_argument("padid", help="the padid")
    p.add_argument("--html", default=None, help="html, default: read from stdin")
    p.add_argument("--padinfo", default="etherpad_info.json", help="settings, default: etherpad_info.json")
    p.add_argument("--showurl", default=False, action="store_true")
    # p.add_argument("--format", default="text", help="output format, can be: text, json; default: text")
    p.add_argument("--create", default=False, action="store_true", help="flag to create pad if necessary")
    p.add_argument("--limit", default=False, action="store_true", help="limit text to 100k (etherpad limit)")
    args = p.parse_args(args)

    with open(args.padinfo) as f:
        info = json.load(f)

    apiurl = info.get("localapiurl", info["apiurl"])
    apikey = info['apikey']

    with open(args.html) as f:
        htmlsrc = f.read()
    # print (type(htmlsrc))
    if args.create:
        resp = pushhtml(apiurl, apikey, args.padid, htmlsrc)
    else:
        resp = sethtml(apiurl, apikey, args.padid, htmlsrc)
    print (resp)
