import re
import sys
import os
import json
from urllib.parse import urlencode, quote as urlquote
from urllib.request import urlopen
from urllib.request import urlopen, URLError, HTTPError
from datetime import datetime
from xml.etree import ElementTree as ET
from fnmatch import fnmatch
from time import sleep 

from etherdump.commands.common import padpath, splitpadname
from etherdump.commands.html5tidy import html5tidy

import html5lib


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

def try_deleting (files):
    for f in files:
        try:
            os.remove(f)
        except OSError as e:
            pass

class Etherpad:
    def __init__(self, apiurl, apikey, verbose=False):
        self.apiurl = apiurl
        self.apikey = apikey
        self.verbose = verbose

    def list (self):
        # apiurl = {0[protocol]}://{0[hostname]}:{0[port]}{0[apiurl]}{0[apiversion]}/".format(info)
        data = {}
        data['apikey'] = self.apikey
        requesturl = self.apiurl+'listAllPads?'+urlencode(data)
        if self.verbose:
            print (requesturl)
        return getjson(requesturl)['data']['padIDs']

    def pad_revisions (self, padid):
        # apiurl = {0[protocol]}://{0[hostname]}:{0[port]}{0[apiurl]}{0[apiversion]}/".format(info)
        data = {}
        data['apikey'] = self.apikey
        data['padID'] = padid
        # print (f"pad_revisions: {padid}")
        requesturl = self.apiurl+'getRevisionsCount?'+urlencode(data)
        if self.verbose:
            print (requesturl)
        return getjson(requesturl)['data']['revisions']

    def pad_last_edited (self, padid):
        data = {}
        data['apikey'] = self.apikey
        data['padID'] = padid
        requesturl = self.apiurl+'getLastEdited?'+urlencode(data)
        if self.verbose:
            print (requesturl)        
        lastedited_raw = int(getjson(requesturl)['data']['lastEdited'])
        lastedited_iso = datetime.fromtimestamp(int(lastedited_raw)/1000).isoformat()
        return lastedited_raw, lastedited_iso

    def pad_author_ids (self, padid):
        data = {}
        data['apikey'] = self.apikey
        data['padID'] = padid
        requesturl = self.apiurl+'listAuthorsOfPad?'+urlencode(data)
        if self.verbose:
            print (requesturl)                
        return getjson(requesturl)['data']['authorIDs']

    def pad_text (self, padid, rev=None, return_url=False, raw=False):
        data = {}
        data['apikey'] = self.apikey
        data['padID'] = padid
        if rev is not None:
            data['rev'] = rev
        requesturl = self.apiurl+'getText?'+urlencode(data)
        if return_url:
            return requesturl
        else:        
            text = getjson(requesturl)
            if raw:
                return text
            assert (text["_code"] == 200)
            return text['data']['text']

    def pad_html (self, padid, rev=None, return_url=False, raw=False):
        data = {}
        data['apikey'] = self.apikey
        data['padID'] = padid
        if rev is not None:
            data['rev'] = rev
        requesturl = self.apiurl+'getHTML?'+urlencode(data)
        if return_url:
            return requesturl
        else:        
            text = getjson(requesturl)
            if raw:
                return text
            assert (text["_code"] == 200)
            return text['data']['html']

    def pad_createDiffHTML (self, padid, return_url=False, raw=False):
        data = {}
        data['apikey'] = self.apikey
        data['padID'] = padid
        data['startRev'] = 0
        requesturl = self.apiurl+'createDiffHTML?'+urlencode(data)
        if return_url:
            return requesturl
        else:        
            text = getjson(requesturl)
            if raw:
                return text
            assert (text["_code"] == 200)
            return text['data']['html']


    def pad_pull (self, padid, \
        pub, group, fix_names, folder, zerorevs, \
        meta, text, html, dhtml, nopublish, 
        output, force, css, script, raw_ext=".raw.txt"):
        # data['padID'] = padid
        p = padpath(padid, pub, group, fix_names)
        if folder:
            p = os.path.join(p, padid) # padid.encode("utf-8")

        metapath = p + ".meta.json"
        revisions = None
        tries = 1
        # padurlbase = re.sub(r"api/1.2.9/$", "p/", info["apiurl"])
        padurlbase = re.sub(r"api/\d+\.\d+\.\d+/$", "p/", self.apiurl)
        meta = {}
        # if type(padurlbase) == unicode:
        #     padurlbase = padurlbase.encode("utf-8")
        while True:
            try:
                if os.path.exists(metapath):
                    with open(metapath) as f:
                        meta.update(json.load(f))
                    # revisions = getjson(info['localapiurl']+'getRevisionsCount?'+urlencode(data))['data']['revisions']
                    revisions = self.pad_revisions(padid)
                    
                    if meta['revisions'] == revisions and not force:
                        return
                
                meta['padid'] = padid # .encode("utf-8")
                versions = meta["versions"] = []
                versions.append({
                    "url": padurlbase + urlquote(padid),
                    "type": "pad",
                    "code": 200
                })

                if revisions == None:
                    # meta['revisions'] = getjson(info['localapiurl']+'getRevisionsCount?'+urlencode(data))['data']['revisions']
                    meta['revisions'] = self.pad_revisions(padid)
                else:
                    meta['revisions' ] = revisions            

                if (meta['revisions'] == 0) and (not zerorevs):
                    # print("Skipping zero revs", file=sys.stderr)
                    return

                # todo: load more metadata!
                meta['group'], meta['pad'] = splitpadname(padid)
                meta['pathbase'] = p
                # meta['lastedited_raw'] = int(getjson(info['localapiurl']+'getLastEdited?'+urlencode(data))['data']['lastEdited'])
                # meta['lastedited_iso'] = datetime.fromtimestamp(int(meta['lastedited_raw'])/1000).isoformat()
                meta['lastedited_raw'], meta['lastedited_iso'] = self.pad_last_edited(padid)
                # meta['author_ids'] = getjson(info['localapiurl']+'listAuthorsOfPad?'+urlencode(data))['data']['authorIDs']
                meta['author_ids'] = self.pad_author_ids(padid)
                break
            except HTTPError as e:
                tries += 1
                if tries > 3:
                    print ("Too many failures ({0}), skipping".format(padid), file=sys.stderr)
                    return
                else:
                    sleep(3)
            except TypeError as e:
                print ("Type Error loading pad {0} (phantom pad?), skipping".format(padid), file=sys.stderr)
                return

        if output:
            print (padid)

        if (meta or text or html or dhtml):
            try:
                os.makedirs(os.path.split(metapath)[0])
            except OSError:
                pass

        # text = getjson(info['localapiurl']+'getText?'+urlencode(data))
        text = self.pad_text(padid, raw=True)
        ##########################################
        ## ENFORCE __NOPUBLISH__ MAGIC WORD
        ##########################################
        if nopublish and nopublish in text['data']['text']:
            # TRY TO PURGE ANY EXISTING DOCS
            print ("NOPUBLISH!", file=sys.stderr)
            try_deleting((p+raw_ext,p+".raw.html",p+".diff.html",p+".meta.json"))
            return

        if text:
            ver = {"type": "text"}
            versions.append(ver)
            ver["code"] = text["_code"]
            if text["_code"] == 200:
                text = text['data']['text']

                ver["path"] = p+raw_ext
                ver["url"] = urlquote(ver["path"])
                with open(ver["path"], "w", errors="surrogatepass") as f:
                    f.write(text)
                # once the content is settled, compute a hash
                # and link it in the metadata!

        links = []
        if css:
            links.append({"href":css, "rel":"stylesheet"})
        # todo, make this process reflect which files actually were made
        versionbaseurl = urlquote(padid)
        links.append({"href":versions[0]["url"], "rel":"alternate", "type":"text/html", "title":"Etherpad"})
        if text:
            links.append({"href":versionbaseurl+raw_ext, "rel":"alternate", "type":"text/plain", "title":"Plain text"})
        if html:
            links.append({"href":versionbaseurl+".raw.html", "rel":"alternate", "type":"text/html", "title":"HTML"})
        if dhtml:
            links.append({"href":versionbaseurl+".diff.html", "rel":"alternate", "type":"text/html", "title":"HTML with author colors"})
        if meta:
            links.append({"href":versionbaseurl+".meta.json", "rel":"alternate", "type":"application/json", "title":"Meta data"})

        # links.append({"href":"/", "rel":"search", "type":"text/html", "title":"Index"})

        if dhtml:
            # data['startRev'] = "0"
            # html = getjson(info['localapiurl']+'createDiffHTML?'+urlencode(data))
            html = self.pad_createDiffHTML(padid, raw=True)
            ver = {"type": "diffhtml"}
            versions.append(ver)
            ver["code"] = html["_code"] 
            if html["_code"] == 200:
                try:
                    html = html['data']['html']
                    ver["path"] = p+".diff.html"
                    ver["url"] = urlquote(ver["path"])
                    # doc = html5lib.parse(html, treebuilder="etree", override_encoding="utf-8", namespaceHTMLElements=False)
                    doc = html5lib.parse(html, treebuilder="etree", namespaceHTMLElements=False)
                    html5tidy(doc, indent=True, title=padid, scripts=script, links=links, viewport_meta="width=device-width,initial-scale=1")
                    with open(ver["path"], "w") as f:
                        # f.write(html.encode("utf-8"))
                        print(ET.tostring(doc, method="html", encoding="unicode"), file=f)
                except TypeError:
                    # Malformed / incomplete response, record the message (such as "internal error") in the metadata and write NO file!
                    ver["message"] = html["message"]
                    # with open(ver["path"], "w") as f:
                    #     print ("""<pre>{0}</pre>""".format(json.dumps(html, indent=2)), file=f)

        # Process text, html, dhtml, all options
        if html:
            # html = getjson(info['localapiurl']+'getHTML?'+urlencode(data))
            html = self.pad_html(padid, raw=True)
            ver = {"type": "html"}
            versions.append(ver)
            ver["code"] = html["_code"]
            if html["_code"] == 200:
                html = html['data']['html']
                ver["path"] = p+".raw.html"
                ver["url"] = urlquote(ver["path"])
                # JUN 2016: chaning to save REALLY the RAW / unchanged HTML from the API
                with open(ver["path"], "w") as f:
                    print(html, file=f)

                # doc = html5lib.parse(html, treebuilder="etree", namespaceHTMLElements=False)
                # html5tidy(doc, indent=True, title=padid, scripts=args.script, links=links)
                # with open(ver["path"], "w") as f:
                #     # f.write(html.encode("utf-8"))
                #     print (ET.tostring(doc, method="html", encoding="unicode"), file=f)

        # output meta
        if meta:
            ver = {"type": "meta"}
            versions.append(ver)
            ver["path"] = metapath
            ver["url"] = urlquote(metapath)
            with open(metapath, "w") as f:
                json.dump(meta, f, indent=2)
        return True



if __name__ == "__main__":
    from argparse import ArgumentParser

    p = ArgumentParser("call listAllPads and print the results")
    p.add_argument("--padinfo", default=".etherdump/settings.json", help="settings, default: .etherdump/settings.json")
    p.add_argument("--showurl", default=False, action="store_true")
    p.add_argument("--format", default="lines", help="output format: lines, json; default lines")
    args = p.parse_args()
    ep = Etherpad(args.padinfo)
    pads = ep.list()
    pads = [x for x in pads if x.endswith(".feed")]
    print(f"{len(pads)} feeds")
