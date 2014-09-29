#!/usr/bin/env python

import argparse
import hashlib
import json
import os.path
import requests
import requests.exceptions
import sys


def looks_like_uri(fn):
    return fn.startswith(("http://", "https://", "youtube:", "yt:"))


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


def send_files(files, config):
    url_base = "http://" + config["host"] + "/srv/v1.0"
    for fn in files:
        if config["verbose"]:
            print("Checking filename/URI {}".format(fn))
        if looks_like_uri(fn):
            pass
        elif os.path.exists(fn):
            song = open(fn, "rb")
            sha1 = hashlib.sha1(song.read()).hexdigest()
            result = send_post(url_base + "/song/" + sha1)
            if result is not None and not result["error"]:
                print("OK")
                continue

            print("File not found on the server, sending")
            song.seek(0)
            result = send_post(url_base + "/file", files={'file': song})
            if result is not None:
                print("File sent successfully, adding to playlist")
                result = send_post(url_base + "/song/" + result["key"])
                if result is not None:
                    print("OK")

        else:
            print("Error: {} is not a supported URI nor an existing file\n".format(fn))
            continue


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
        # TODO: Generate configuration stub if missing
        print("Error: The configuration file does not exist.")
        sys.exit(1)

    # Load the configuration
    cfg = json.load(open(args.config, "r"))
    cfg["verbose"] = args.verbose

    if args.cmd == "play":
        send_files(args.files, cfg)

    elif args.cmd == "np":
        send_np(cfg)

    elif args.cmd == "playlist":
        send_playlist(args.n, cfg)

    elif args.cmd == "skip":
        send_skip(cfg)

    elif args.cmd == "clear":
        send_clear(cfg)