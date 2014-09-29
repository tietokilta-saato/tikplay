#!/usr/bin/env python

import argparse
import hashlib
import importlib
import os.path
import requests
import sys

def looks_like_uri(fn):
    return fn.startswith(("http://", "https://", "youtube:", "yt:"))

def send_request(files, config):
    for fn in files:
        if config["verbose"]:
            print("Checking filename/URI {}".format(fn))
        if looks_like_uri(fn):
            pass
        elif os.path.exists(fn):
            sha1 = hashlib.sha1(open(fn, "rb").read()).hexdigest()
            data = requests.post(config["host"] + "/srv/v1.0/playsong", {"song_sha1": sha1}).json
        else:
            print("Error: {} is not a supported URI nor an existing file\n".format(fn))
            continue

if __name__ == "__main__":
    # Parse the arguments
    parser = argparse.ArgumentParser(prog="tikplay", description="tikplay - play that funky music")
    parser.add_argument('files', metavar='file/url', type=str, nargs='+', help='path to file or URL')
    parser.add_argument('-v', '--verbose', action='store_true', help='be verbose for the gory details')
    parser.add_argument('-c', '--config', action='store', nargs=1, default=os.path.expanduser('~/.tikplayrc.py'),
                        help='specify the configuration file')

    args = parser.parse_args(sys.argv)
    if not os.path.exists(args["config"]):
        # TODO: Generate configuration stub if missing
        print("Error: The configuration file does not exist.")
        sys.exit(1)

    # Load the configuration
    sys.path[0:0] = [os.path.dirname(os.path.expanduser(args["config"]))]
    config = importlib.import_module(os.path.basename(args["config"].rsplit(".", 1)[0]))
    sys.path = sys.path[1:]

    if args["verbose"]:
        config["verbose"] = True

    send_request(args["files"], config)