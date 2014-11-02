#!/usr/bin/env python

import argparse
import hashlib
import json
import os
import os.path
import platform
import requests
import requests.exceptions
import sys

try:
    import pwd
    pwd_available = True
except ImportError:
    import getpass
    pwd_available = False


def whoami():
    # Prefer the pwd module, which is available only on Unix systems, as getpass relies on environment variables
    node = platform.node()
    if not node:
        node = "unknown"
    if pwd_available:
        return "{}@{}".format(pwd.getpwuid(os.getuid())[0], node)
    return "{}@{}".format(getpass.getuser(), node)


def wrap_request(method, *args_, **kwargs):
    data = None
    try:
        data = method(*args_, **kwargs)
        return data.json()
    except requests.exceptions.ConnectionError as e:
        print("Connection error: " + str(e))
    except ValueError:
        print("Invalid JSON received: " + data.text)


def send_post(url, **kwargs):
    return wrap_request(requests.post, url, **kwargs)


def send_get(url, **kwargs):
    return wrap_request(requests.get, url, **kwargs)


def send_delete(url, **kwargs):
    return wrap_request(requests.delete, url, **kwargs)


def send_song(files, config):
    url_base = "http://" + config["host"] + "/srv/v1.0"
    for fn in files:
        data = {
            "user": whoami()
        }

        if config["verbose"]:
            print("Checking filename/URI {}".format(fn))

        # URI
        if not os.path.exists(fn):
            data["url"] = fn
            result = send_post(url_base + "/song", data=json.dumps(data))
            if result is not None:
                print(result["text"])
            return

        # File
        data["filename"] = os.path.basename(fn)
        song = open(fn, "rb")
        sha1 = hashlib.sha1(song.read()).hexdigest()
        data["url"] = "sha1:" + sha1
        result = send_post(url_base + "/song", data=json.dumps(data))
        if result is not None and not result["error"]:
            print(result["text"])
            continue

        print("File not found on the server, sending")
        song.seek(0)
        result = send_post(url_base + "/file", files={'file': song})
        if result is not None:
            print("File sent successfully, adding to playlist")
            data["url"] = result["key"]
            result = send_post(url_base + "/song", data=json.dumps(data))
            if result is not None:
                print(result["text"])


def send_np(config):
    result = send_get("http://" + config["host"] + "/srv/v1.0/song")
    print(result)


def send_playlist(_, config):
    result = send_get("http://" + config["host"] + "/srv/v1.0/queue")
    print(result)


def send_skip(config):
    result = send_delete("http://" + config["host"] + "/srv/v1.0/song")
    print(result)


def send_clear(config):
    result = send_delete("http://" + config["host"] + "/srv/v1.0/queue")
    print(result)


def gen_config(target, **kwargs):
    with open(target, 'w') as f:
        json.dump(kwargs, f, indent=4)


if __name__ == "__main__":
    # Parse the arguments
    parser = argparse.ArgumentParser(prog="tikplay", description="tikplay - play that funky music")
    parser.add_argument('-v', '--verbose', action='store_true', help='be verbose for the gory details')
    parser.add_argument('-c', '--config', action='store', nargs=1, default=os.path.expanduser('~/.tikplayrc'),
                        help='specify the configuration file')

    sub = parser.add_subparsers(dest='cmd', help="sub-command help")
    play_parser = sub.add_parser('play', help='play a song')
    play_parser.add_argument('files', metavar='file/url', type=str, nargs='+', help='path to file or URL')
    np_parser = sub.add_parser('np', help='now playing')
    pl_parser = sub.add_parser('playlist', help='playlist')
    pl_parser.add_argument('n', default=10, type=int, help='amount of entries to fetch')
    del_parser = sub.add_parser('skip', help='skip song')
    clear_parser = sub.add_parser('clear', help='clear playlist')

    args = parser.parse_args(sys.argv[1:])
    if not os.path.exists(args.config):
        print("Error: The configuration file does not exist. Generating a default config to %s" % args.config)
        gen_config(args.config, verbose=True, host="tikradio.tt.hut.fi:5000")

    # Load the configuration
    with open(args.config, 'r') as fp:
        cfg = json.load(fp)

    cfg["verbose"] = args.verbose

    if args.cmd == "play":
        send_song(args.files, cfg)

    elif args.cmd == "np":
        send_np(cfg)

    elif args.cmd == "playlist":
        send_playlist(args.n, cfg)

    elif args.cmd == "skip":
        send_skip(cfg)

    elif args.cmd == "clear":
        send_clear(cfg)
