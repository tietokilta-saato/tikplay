from flask import request, jsonify, current_app
from flask.ext.restful import Resource
from werkzeug.utils import secure_filename
import os
from hashlib import sha1


__version__ = 'v1.0'
url_base = '/srv/{}'.format(__version__)
ALLOWED_EXTENSIONS = {'mp3', 'ogg', 'wav'}


class File(Resource):
    def __allowed_file(self, file):
        return file.filename.split('.')[-1] in ALLOWED_EXTENSIONS

    def post(self):
        """
        POST a new song to save
        """
        file = request.files['file']
        filename = secure_filename(file.filename)
        if file and self.__allowed_file(file):
            calced_hash = sha1(file.stream.read()).hexdigest()
            file.stream.seek(0)
            _filename = "{}.{}".format(calced_hash, file.filename.split('.')[-1])
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], _filename))
            return jsonify(filename=filename, saved=True, key=calced_hash,
                           text="File successfully saved as {}. Use this as key to play this file".format(calced_hash))

        elif not self.__allowed_file(file):
            return jsonify(filename=filename, saved=False, text="Filetype not allowed!")

        else:
            return jsonify(filename="", saved=False,
                           text="You have to send a file, e.g. curl -X POST -F file=\"@<file>\" <server_address>")


class NowPlaying(Resource):
    def get(self):
        """
        GET now playing song
        """
        audio_api = current_app.config['audio_api']
        return jsonify(text=audio_api.now_playing(queue_length=1))

    def delete(self):
        """
        DELETE now playing song (i.e. skip a song)
        """
        audio_api = current_app.config['audio_api']
        return jsonify(text=audio_api.next_())


class Queue(Resource):
    def get(self):
        """
        GET the now_playing queue
        """
        audio_api = current_app.config['audio_api']
        return jsonify(text=audio_api.now_playing())

    def delete(self):
        audio_api = current_app.config['audio_api']
        return jsonify(text=audio_api.kill())


class PlaySong(Resource):
    def post(self, song_sha1):
        """
        POST a new song to play. Do

        Keyword arguments:
            song_sha1: identifying SHA1 hash calculated from the file
        """
        audio_api = current_app.config['audio_api']
        result = None
        text = ""
        try:
            result = audio_api.play(song_sha1)
            if result is None:
                text = "Song not found, please upload it"
        except Exception as e:
            text = str(e)

        if result is None:
            return jsonify(error=True, text=text)
        return jsonify(sha1=song_sha1, playing=result, error=False)


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
