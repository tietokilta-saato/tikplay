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


class Queue(Resource):
    def get(self):
        """
        GET the now_playing queue
        """
        audio_api = current_app.config['audio_api']
        pass


class PlaySong(Resource):
    def post(self, song_sha1):
        """
        POST a new song to play. Do

        Keyword arguments:
            song_sha1: identifying SHA1 hashsum calculated from the file
        """
        audio_api = current_app.config['audio_api']
        cache_handler = current_app.config['audio_api']
        try:
            result = audio_api.play(song_sha1)
            cache_handler.play(song_sha1)
            return jsonify(sha1=song_sha1, playing=result, error=False)
        except AVbinException:
            return jsonify(sha1=song_sha1, playing=False, error=True,
                           text='Song not found. Try finding the song first!')


class Find(Resource):
    def get(self, find_type, find_key):
        """
        GET find a song from the database.

        Keyword arguments:
            find_type: valid values 1 (song_hash), 2 (artist), 3 (title), 4 (length), 5 (filename)
            find_key: value corresponding to the type: 1 (SHA1), 2 (String),
                      3 (String), 4 (Integer (seconds)), 5 (filename)
        """
        methods = ['song_hash', 'artist', 'title', 'length', 'filename']
        cache_handler = current_app.config['cache_handler']
        # find_type is ints from 1 - 5, list indices are ints from 0 - 4
        found = cache_handler.find(methods[find_type - 1], find_key)
        if found is not None:
            return jsonify(find_type=methods[find_type - 1], find_key=find_key, found=True, text=str(found))
        else:
            return jsonify(find_type=methods[find_type - 1], find_key=find_key, found=False)
