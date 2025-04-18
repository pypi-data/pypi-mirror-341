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

def parse_yaml (src):
    data = None
    text = src
    try:
        for i, d in enumerate(yaml.load_all(src, Loader=yaml.Loader)):
            # print (f"ITEM{i}:", type(d), d)
            if i == 0 and type(d) == dict:
                data = d
            elif i == 1 and type(d) == str:
                text = d
    except yaml.YAMLError as ex:
        print (f"YAML PARSE ERROR ({ex})")
    return data, text
