import argparse
import logging
import os

import mpd
from flask import Flask
from flask.ext import restful

import audio
import cache
import server
import watcher
from songlogger import SongLogger

logging.basicConfig(
    level=logging.DEBUG
)

# Parse args
_argparser = argparse.ArgumentParser()
_argparser.add_argument('-df', '--debug-flask', help='Enable flask debug mode', default=False, action='store_true')
_argparser.add_argument('-tf', '--testing-flask', help='Enable flask testing mode', default=False, action='store_true')
_argparser.add_argument('-D', '--daemon', help="Fork in to the background", default=False, action='store_true')
_argparser.add_argument('-p', '--port', help='Port that we should listen (Default: 5000)', type=int, default=5000)
_argparser.add_argument('-s', '--song-dir',
                        help='Directory to which store technical copies of the songs (Default: ~/.tikplay/music)',
                        type=str,
                        default='~/.tikplay/music')
_argparser.add_argument('-l', '--log-file',
                        help='The song log file to use (Default: ~/.tikplay/log)',
                        type=str,
                        default='~/.tikplay/log')
args = _argparser.parse_args()

# Daemonize
workdir = os.path.abspath(os.path.expanduser(args.song_dir))
if not os.path.exists(workdir):
    os.mkdir(workdir)

if args.daemon:
    import sys
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError as e:
        print('Fork failed: {0} ({1})'.format(e.errno, e.strerror))
        sys.exit(1)

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

# Ensure that the cache directory and the subdirectory for file uploads (ie. sha1) exist
args.song_dir = os.path.expanduser(args.song_dir)
if not os.path.exists(args.song_dir):
    os.makedirs(args.song_dir)
if not os.path.exists(os.path.join(args.song_dir, "sha1")):
    os.makedirs(os.path.join(args.song_dir, "sha1"))

# Init classes
task_dict = {}
cache_handler = cache.Cache(args.song_dir)
audio_api = audio.API(media_cls=mpd, mpd_addr=("localhost", 6600))
songlogger = SongLogger(args.log_file)

# Init the watcher
watcher_thread = watcher.TaskWatcher(task_dict, cache_handler, audio_api, songlogger)
watcher_thread.start()

# Init flask
url_base = server.url_base

tikserver = Flask('tikplay')
tikserver.debug = args.debug_flask
tikserver.testing = args.testing_flask

tikserver.config['song_dir'] = args.song_dir
tikserver.config['task_dict'] = task_dict
tikserver.config['cache_handler'] = cache_handler
tikserver.config['audio_api'] = audio_api
tikserver.config['songlogger'] = songlogger
tikserver.config['UPLOAD_FOLDER'] = os.path.join(args.song_dir, "sha1")

tikserver_api = restful.Api(tikserver)
tikserver_api.cache = cache.Cache(args.song_dir)
tikserver_api.add_resource(server.File, '{}/file'.format(url_base))
tikserver_api.add_resource(server.Song, '{}/song'.format(url_base))
tikserver_api.add_resource(server.Queue, '{}/queue'.format(url_base))
tikserver_api.add_resource(server.Queue, '{}/queue/<int:length>'.format(url_base))
tikserver_api.add_resource(server.Task, '{}/task/<int:id_>'.format(url_base))
tikserver_api.add_resource(server.Find, '{}/find/<int:find_type>/<string:find_key>'.format(url_base))
tikserver.run(port=args.port)
