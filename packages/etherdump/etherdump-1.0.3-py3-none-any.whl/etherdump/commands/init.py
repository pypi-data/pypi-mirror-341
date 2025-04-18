# from argparse import ArgumentParser
import click
from urllib.parse import urlparse, urlunparse, urlencode
from urllib.request import urlopen, URLError, HTTPError
import json, os, sys


def get_api(url, cmd=None, data=None, verbose=False):
    try:
        useurl = url+cmd
        if data:
            useurl += "?"+urlencode(data)
        if verbose:
            print ("trying", useurl, file=sys.stderr)
        resp = urlopen(useurl).read()
        resp = resp.decode("utf-8")
        resp = json.loads(resp)
        if "code" in resp and "message" in resp:
            return resp
    except ValueError as e:
        if verbose:
            print ("  ValueError", e, file=sys.stderr)
        return
    except HTTPError as e:
        if verbose:
            print ("  HTTPError", e, file=sys.stderr)
        if e.code == 401:
            # Unauthorized is how the API responds to an incorrect API key
            return {"code": 401, "message": e}

def tryapiurl (url, verbose=False):
    """
    Try to use url as api, correcting if possible.
    Returns corrected / normalized URL, or None if not possible
    """
    try:
        scheme, netloc, path, params, query, fragment = urlparse(url)
        if scheme == "":
            url = "http://" + url
        scheme, netloc, path, params, query, fragment = urlparse(url)            
        params, query, fragment = ("", "", "")
        path = path.strip("/")
        # 1. try directly...
        apiurl = urlunparse((scheme, netloc, path, params, query, fragment))+"/"
        if get_api(apiurl, "listAllPads", verbose=verbose):
            return apiurl
        # 2. try with += api/1.2.9
        path = os.path.join(path, "api", "1.2.9")+"/"
        apiurl = urlunparse((scheme, netloc, path, params, query, fragment))
        if get_api(apiurl, "listAllPads", verbose=verbose):
            return apiurl
    # except ValueError as e:
    #     print ("ValueError", e, file=sys.stderr)
    except URLError as e:
        print ("URLError", e, file=sys.stderr)

@click.command("initialize an etherdump settings file")
@click.option("--padinfo", default="etherpad_info.json", help="settings file to create, default: etherpad_info.json")
@click.option("--padurl", prompt="URL of the etherpad (or api)")
@click.option("--apikey", prompt="APIKEY")
@click.option("--verbose/--not-verbose", default=False)
@click.option("--reinit/--no-reinit", default=False)
def main(padinfo, padurl, apikey, verbose, reinit):
    padinfo_path = padinfo
    try:
        with open(padinfo) as f:
            padinfo = json.load(f)
        if not reinit:
            print ("File already exists. Use --reinit to reset settings.")
            sys.exit(0)
    except (IOError, ValueError):
        padinfo = {}

    apiurl = padurl
    while True:
        if apiurl:
            apiurl = tryapiurl(apiurl,verbose=verbose)
        if apiurl:
            break
        apiurl = click.prompt("Please type the URL of the etherpad").strip()
    padinfo["apiurl"] = apiurl

    while True:
        if apikey:
            resp = get_api(apiurl, "listAllPads", {"apikey": apikey}, verbose=verbose)
            if resp and resp["code"] == 0:
                break
        click.echo("The APIKEY is the contents of the file APIKEY.txt in the etherpad folder", file=sys.stderr)
        apikey = click.prompt("Please paste the APIKEY").strip()
    padinfo["apikey"] = apikey

    with open(padinfo_path, "w") as f:
        json.dump(padinfo, f, indent=2)

    click.echo(f"Settings stored in {click.style(padinfo_path, bold=True)}")
    click.echo(f"{click.style('Make sure that this file is not PUBLICLY ACCESSIBLE', bold=True)} and specify its location using the {click.style('--padinfo', italic=True)} option of etherdump subcommands.")
