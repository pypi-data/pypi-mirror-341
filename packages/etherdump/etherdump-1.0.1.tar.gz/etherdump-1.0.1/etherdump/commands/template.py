import argparse, sys, json, os
# from urllib.parse import quote as urlquote
from jinja2 import Template, DictLoader, Environment, FileSystemLoader, Markup
import time, datetime # , isodate
from xml.etree import ElementTree as ET

import html5lib# , markdown
# from .timecode import timecode_fromsecs as timecode


def strftime (t, format='%Y-%m-%d %H:%M:%S'):
    return time.strftime(format, time.localtime(t))

def isotime (t):
    return datetime.datetime.fromtimestamp(t).isoformat()

# def isoduration (t):
#     return isodate.duration_isoformat(datetime.timedelta(0, t))


def forcelist (x):
    if type(x) == dict:
        return [x]
    return x

def merge (a, b):
    out = a + b
    return sorted(out, key=lambda x: (x['id'].lower(), x['id']))

def innerHTML (elt):
    if elt.text != None:
        ret = elt.text
    else:
        ret = u""
    return ret + u"".join([ET.tostring(x, method="html", encoding="unicode") for x in elt])

def add_attribute_to_links (src, attrname, attrvalue):
    t = html5lib.parseFragment(src, treebuilder="etree", namespaceHTMLElements=False)
    for a in t.findall(".//a"):
        a.attrib[attrname]=attrvalue
    return innerHTML(t)

def filename2title (f):
    f, _ = os.path.splitext(f)
    return f.replace("_", " ")

def wbr_underscores (f):
    return f.replace("_", "_<wbr>")

def main (args):
    p = argparse.ArgumentParser("")
    p.add_argument("--output", default=sys.stdout, type=argparse.FileType("w"))
    p.add_argument("template")
    p.add_argument("--data", type=argparse.FileType('r'), default=sys.stdin)
    p.add_argument("--listkey", default="items", help="if incoming data is a list, give it this name for the template, default: items")
    p.add_argument("--set", nargs=2, default=None, action="append")
    args = p.parse_args(args)
    # print ("args", args)
    data = json.load(args.data)
    tpath, tname = os.path.split(args.template)
    env = Environment(loader=FileSystemLoader(tpath))

    # # count the occurences of allkeys in files
    # allkeys = {}
    # for item in data['files']:
    #     for key in item:
    #         if key not in allkeys:
    #             allkeys[key] = 0
    #         allkeys[key]+=1
        
    # import jinjafilters
    # for name, fn in jinjafilters.all.items():
    env.filters['strftime'] = strftime
    env.filters['isotime'] = isotime
    # env.filters['isoduration'] = isoduration
    # env.filters['timecode'] = timecode
    env.filters['forcelist'] = forcelist
    env.filters['merge'] = merge
    # md = markdown.Markdown(extensions=['meta'])
    # env.filters['markdown'] = lambda text: Markup(md.convert(text))
    env.filters['add_attribute_to_links'] = lambda text, name, value: Markup(add_attribute_to_links(text, name, value))
    env.filters['filename2title'] = filename2title
    env.filters['wbr_'] = lambda x: Markup(wbr_underscores(x))

    # if args.meta:
    #     for m in args.meta:
    #         try:
    #             with open(m) as f:
    #                 meta = json.load(f)
    #                 for key,value in meta.items():
    #                     data[key] = value
    #         except FileNotFoundError:
    #             print ("Metadata {} not found".format(m), file=sys.stderr)
    template = env.get_template(tname)
    if type(data) == list:
        # print ("Detected list, adding as {0}".format(args.listkey), file=sys.stderr)
        data = {
            args.listkey: data
        }
    if args.set:
        for key, value in args.set:
            print ("Setting {0}={1}".format(key, value), file=sys.stderr)
            data[key] = value

#    data['allkeys'] = allkeys
    print (template.render(**data), file=args.output)

def add_subparser (subparsers):
    p = subparsers.add_parser('template', help='Combine json files')
    p.add_argument("--output", default=sys.stdout, type=argparse.FileType("w"))
    p.add_argument("template")
    p.add_argument("--data", type=argparse.FileType('r'), default=sys.stdin)
    p.add_argument("--listkey", default="items", help="if incoming data is a list, give it this name for the template, default: items")
    p.add_argument("--set", nargs=2, default=None, action="append")
    # p.add_argument("--meta", help="Mixin this metadata", action="append")
    p.set_defaults(func=main)

if __name__ == "__main__":
    print ("MAIN:TEMPLATE")
    import argparse
    p = argparse.ArgumentParser("")
    subparsers = p.add_subparsers(help="subcommands")
    add_subparser(subparsers)
    main(p.parse_args(args=(["template"] + sys.argv[1:])))

