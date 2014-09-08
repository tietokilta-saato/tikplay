from flask import request, jsonify, current_app
from flask.ext.restful import Resource
from werkzeug.utils import secure_filename
from pyglet.media.avbin import AVbinException
import os
from hashlib import sha1


__version__ = 'v1.0'
url_base = '/srv/{}'.format(__version__)
ALLOWED_EXTENSIONS = set(['mp3', 'ogg', 'wav'])


class File(Resource):
    def __allowed_file(self, file):
        return file.filename.split('.')[-1] in ALLOWED_EXTENSIONS

    def post(self):
        """
        POST a new song to save
        """
        cache_handler = current_app.config['cache_handler']
        audio_api = current_app.config['audio_api']
        file = request.files['file']
        if file and self.__allowed_file(file):
            filename = secure_filename(file.filename)
            calced_hash = sha1(file)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], calced_hash))
            try:
                song_meta = audio_api.get_metadata(calced_hash)
            except AVbinException:
                return jsonify(filename=filename, saved=None, text='Something weird happened, try again')

            cache_handler.store(calced_hash, filename, **song_meta)
            return jsonify(filename=filename, saved=True,
                           text="File successfully saved as {}! Use this key to play this file".format(calced_hash))

        elif not self.__allowed_file(file):
            return jsonify(filename=filename, saved=False, text="Filetype not allowed!")

        else:
            return jsonify(filename="", saved=False,
                           text="You have to send a file, e.g. curl -X POST -F file=@<file> <server_address>")


class NowPlaying(Resource):
    def get(self):
        """
        GET now playing song
        """
        audio_api = current_app.config['audio_api']
        return "hello world"


class PlaySong(Resource):
    def post(self, song_sha1):
        """
        POST a new song to play
        """
        audio_api = current_app.config['audio_api']
        return song_sha1


class Queue(Resource):
    def get(self):
        """
        GET the now_playing queue
        """
        audio_api = current_app.config['audio_api']
        pass


class Find(Resource):
    def get(self, find_type, find_key):
        """
        GET find a song from the database.

        Keyword arguments:
            find_type: valid values 1 (song_hash), 2 (artist), 3 (title), 4 (length), 5 (filename)
            find_key: ...
        """
        cache_handler = current_app.config['cache_handler']
        return "{} {}".format(find_type, find_key)
