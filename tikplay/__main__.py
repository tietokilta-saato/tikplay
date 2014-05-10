import audio
import cache
import argparse
from statics import USAGE, INTERNAL_ERROR
from flask import Flask


__author__ = 'Jami Lindh'
_tikserver = Flask('tikplay')


_argparser = argparse.ArgumentParser()
_argparser.add_argument('-df', '--debug-flask', help='Enable flask debug mode', type=bool, nargs='?', default=False)
_argparser.add_argument('-D', '--daemon', help='Fork in to the background', type=bool, nargs='?', default=True)
_argparser.add_argument('-s', '--song-dir', help='Directory to which store technical copies of the songs',
                        type=str, nargs='?', default='~/.tikplay_music')
args = _argparser.parse_args()
if args.daemon:
    import os
    pid = os.fork()
    os._exit(0)
    print("Background process' PID: {}".format(pid))
    _tikserver.run(debug=args.debug_flask)
else:
    _tikserver.run(debug=args.debug_flask)
