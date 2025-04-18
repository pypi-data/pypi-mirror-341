import argparse
import sys
import yaml
import re
import json



def parse_args (match, d):
    d['ordered'] = []
    d['by_name'] = {}
    for part in match.split("|"):
        part = part.strip()
        if "=" in part:
            name, value = part.split("=", 1)
            name = name.strip()
            value = value.strip()
            d['ordered'].append(value)
            d['by_name'][name] = value
        else:
            value = part
            d['ordered'].append(value)
    return d

def scan(text):
    for m in pat.finditer(text):
        d = {}
        mw1, mw2, args = m.groups()
        print ("args", args)
        d['name'] = mw1 or mw2
        if args:
            args = parse_args(args, d)
    yield d

def parse_yaml(src):
    data = None
    text = src
    parts = re.split(r"---\n", src)
    parts = [x.strip() for x in parts]
    parts = [x for x in parts if x]
    if len(parts) > 1:
        try:
            data = yaml.load(parts[0])
            text = "---\n".join(parts[1:])
        except yaml.YAMLError as ex:
            print (f"YAML PARSE ERROR ({ex})")
            # keep text = src
        # join the rest
        
    return data,text

# def parse_yaml (src):
#     data = None
#     text = src
#     try:
#         for i, d in enumerate(yaml.load_all(src, Loader=yaml.Loader)):
#             # print (f"ITEM{i}:", type(d), d)
#             if i == 0 and type(d) == dict:
#                 data = d
#             elif i == 1 and type(d) == str:
#                 text = d
#     except yaml.YAMLError as ex:
#         print (f"YAML PARSE ERROR ({ex})")
#     return data, text

# def load_magic_words ():
#     from importlib import import_module
#     if "." not in sys.path:
#         sys.path.append(".")
#     return import_module("magicwords")

def process(input, output, magicwords):
    # mdefs = load_magic_words()
    magicwords = {}
    magicwords['by_word'] = {}
    magicwords['ordered'] = []
    words = []
    def mysub (m):
        word = m.groupdict()['word']
        magicwords['ordered'].append(word)
        if word not in magicwords['by_word']:
            magicwords['by_word'][word] = []
        magicwords['by_word'][word].append(word)
        # return f"""<span class="magicword">{word}</span>""" 
        return ""
    markdown_src = ""
    for line_in in input:
        # line_in = line.rstrip()
        line_out = re.sub(r"__(?P<word>\w+)__", mysub, line_in)
        # output line if no subs, OR post substitution, line still has content
        # aka lines with only magic words will be removed
        if line_in == line_out or line_out.strip() != '':
            markdown_src += line_out
            # print(line_out, file=fout)

    # markdown_src = input.read()
    markdown_metadata, text = parse_yaml(markdown_src)
    if not markdown_metadata:
        markdown_metadata = {}
    if 'NOPUBLISH' in magicwords['by_word']:
        markdown_metadata['access'] = "private"

    # if there is data: rebuild source
    if markdown_metadata:
        markdown_src = f"---\n{yaml.dump(markdown_metadata)}---\n{text}"""

    # RUN MULTI
    # p = subprocess.run(["python3", "scripts/multi.py"], input=markdown_src.encode("utf-8"), capture_output=True)
    # markdown_src = p.stdout.decode("utf-8")
    # print (f"markdown_src: {markdown_src}")
    print (markdown_src, file=output, end="")
    if magic:
        with open(magic, "w") as magic_out:
            print (json.dumps(magicwords), file=magic_out)        

def main (args):
    import importlib
    import pkgutil
    import os
    import sys

    # print ("HELLO", file=sys.stderr)
    p = argparse.ArgumentParser(description="preprocess", epilog="""
Takes a document, applies magicwords, outputs json + (markdown) text
""")
    p.add_argument("--input", type=argparse.FileType("r"), default=sys.stdin)
    p.add_argument("--output", type=argparse.FileType("w"), default=sys.stdout)
    p.add_argument("--localmagic", default=False, action="store_true", help="search for magicwords in current directory (be careful)")
    args = p.parse_args(args)
    # print(args)

    from etherdump import magicwords
    allmagic = [magicwords]

    if args.localmagic:
        path = os.getcwd()
        sys.path.append("")
        for finder, name, ispkg in pkgutil.iter_modules([path]):
            if name == "magicwords":
                print (f"importing local magicwords", sys.stderr)
                magicwords_local = importlib.import_module(name)
                allmagic.append(magicwords_local)

    process(args.input, args.output, allmagic)


