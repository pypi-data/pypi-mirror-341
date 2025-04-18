import os
import sys

from .etherpad import Etherpad, getjson

DATAPATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")

usage = """Usage:
    etherdump CMD

where CMD could be:
    appendmeta
    creatediffhtml
    deletepad
    dumpcsv
    gethtml
    gettext
    html5tidy
    index
    init
    join
    listauthors
    list
    pull
    pushhtml
    revisionscount
    sethtml
    settext
    showmeta
    status

For more information on each command try:
    etherdump CMD --help

"""

def main ():
    try:
        cmd = sys.argv[1]
        if cmd.startswith("-"):
            cmd = "sync"
            args = sys.argv
        else:
            args = sys.argv[2:]
    except IndexError:
        print (usage)
        sys.exit(0)
    try:
        # http://stackoverflow.com/questions/301134/dynamic-module-import-in-python
        cmdmod = __import__("etherdump.commands.%s" % cmd, fromlist=["etherdump.commands"])
        cmdmod.main(args)
    except ImportError as e:
        print ("Error performing command '{0}'\n(python said: {1})\n".format(cmd, e))
        print (usage)
