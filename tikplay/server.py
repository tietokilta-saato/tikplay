from flask.ext.restful import Resource
from statics import USAGE, INTERNAL_ERROR
import audio
import cache


__version__ = 'v1.0'
url_base = '/srv/{}'.format(__version__)


class File(Resource):
    def post(self):
        """
        POST a new song to save
        """
        pass


class NowPlaying(Resource):
    def get(self):
        """
        GET now playing song
        """
        return "hello world"


class PlaySong(Resource):
    def post(self, song_sha1):
        """
        POST a new song to play
        @param song_sha1 the sha1 of the song
        """
        return song_sha1


class Queue(Resource):
    def get(self):
        """
        GET the now_playing queue
        """
        pass


class Find(Resource):
    def get(self, find_type, find_key):
        """
        GET find a song from the database.
        @param find_type find from which column
        valid values 1 (song_hash), 2 (artist), 3 (title), 4 (length), 5 (filename)
        @param find_key the key with which to find
        """
        return "{} {}".format(find_type, find_key)
