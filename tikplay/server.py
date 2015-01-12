import json
import os
from hashlib import sha1

from flask import request, jsonify, current_app
from flask.ext.restful import Resource
import time
from werkzeug.utils import secure_filename

import traceback
from audio import play_file
from provider.provider import Provider
from provider.task import TaskState
from utils import is_uri, is_url


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
            if not _filename.endswith(".mp3"):
                _filename += ".mp3"
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], _filename))
            current_app.config['audio_api'].update()
            time.sleep(2.0)  # Whoo, ugly hacks
            return jsonify(filename=filename, saved=True, key="sha1:" + calced_hash,
                           text="File successfully saved as {}. Use this as key to play this file".format(calced_hash))

        elif not self.__allowed_file(file):
            return jsonify(filename=filename, saved=False, text="Filetype not allowed!")

        else:
            return jsonify(filename="", saved=False,
                           text="You have to send a file, e.g. curl -X POST -F file=\"@<file>\" <server_address>")


class Queue(Resource):
    def get(self, length=10):
        """
        GET the now_playing queue
        """
        audio_api = current_app.config['audio_api']
        return jsonify(text=audio_api.now_playing(queue_length=length))

    def delete(self):
        audio_api = current_app.config['audio_api']
        return jsonify(text=audio_api.kill())


class Song(Resource):
    def __init__(self):
        super()
        self.prov = Provider(conf={'download_dir': current_app.config['song_dir']})
        self.cache = current_app.config['cache_handler']

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

    def post(self):
        """
        POST a new song to play by URI/URL.
        """

        try:
            data = json.loads(request.data.decode())
        except ValueError:
            return jsonify(error=True, text="Invalid JSON given")

        uri = data["url"]
        if not uri:
            return jsonify(error=True, text="Invalid URI")

        if is_url(uri):
            uri = self.prov.canonicalize(uri)

        elif not is_uri(uri):
            return jsonify(error=True, text="Invalid URI")

        audio_api = current_app.config['audio_api']
        fn = self.cache.get_song(uri)
        if fn is not None:
            return play_file(
                audio_api, current_app.config['songlogger'], fn, data.get("filename", uri), user=data["user"]
            )

        try:
            task = self.prov.get(uri)
        except ValueError:
            return jsonify(error=True, text="No provider found for " + uri)

        if task.state == TaskState.exception:
            return jsonify(error=True, text=traceback.format_exception_only(type(task.exception), task.exception))

        current_app.config['task_dict'][task.id] = task
        task.metadata['user'] = data.get('user', 'anonymous')
        task.metadata['original_filename'] = data.get('filename', uri)
        return jsonify(error=False, task=task.id, text="Task received, fetching song")


class Task(Resource):
    def get(self, id_):
        """
        GET information about a task.
        :param id_: Task ID
        :return:
        """

        task = current_app.config['task_dict'].get(int(id_), None)
        if task is None:
            return jsonify(error=True, text="Task not found")
        return jsonify(id=task.id, state=task.state, url=task.url)


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
