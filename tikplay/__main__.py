import audio
import cache
import argparse
from statics import USAGE, INTERNAL_ERROR
from server import TikplayFlask, File, Song, Queue, Find, url_base

__author__ = 'Jami Lindh'


_argparser = argparse.ArgumentParser()
_argparser.add_argument('-df', '--debug-flask', help='Enable flask debug mode', default=False, action='store_true')
_argparser.add_argument('-tf', '--testing-flask', help='Enable flask testing mode', default=False, action='store_true')
_argparser.add_argument('-D', '--daemon', help="Fork in to the background", default=False, action='store_true')
_argparser.add_argument('-p', '--port', help='Port that we should listen (Default: 5000)', type=int, default=5000)
_argparser.add_argument('-s', '--song-dir', help='Directory to which store technical copies of the songs (Default: ~/.tikplay_music)',
                        type=str, default='~/.tikplay_music')
args = _argparser.parse_args()

if args.daemon:
    import sys
    import os
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError as e:
        print('Fork failed: {0} ({1})'.format(e.errno, e.strerror))
        sys.exit(1)

    workdir = os.path.expanduser(args.song_dir)
    if not os.path.exists(workdir):
        os.mkdir(workdir)

    os.chdir(workdir)
    os.setsid()
    os.umask(0)

    try:
        pid = os.fork()
        if pid > 0:
            print("Background process' PID: {}".format(pid))
            sys.exit(0)
    except OSError as e:
        print('Fork failed: {0} ({1})'.format(e.errno, e.strerror))
        sys.exit(1)


_tikserver = TikplayFlask('tikplay')
_tikserver.song_dir = args.song_dir
_tikserver.debug = args.debug_flask
_tikserver.testing = args.testing_flask
# TODO: Doesn't work like this for some reason
#_tikserver.view_functions = {'{}/file'.format(url_base), File.as_view('file'),
#                             '{}/song'.format(url_base), Song.as_view('song'),
#                             '{}/queue'.format(url_base), Queue.as_view('queue'),
#                             '{}/find'.format(url_base), Find.as_view('find')}
_tikserver.run(port=args.port)
