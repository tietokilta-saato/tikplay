import datetime
import http.server
import logging
import pysoundcard
import pysoundfile
import threading
from tikplay.statics import USAGE
from tikplay.database import interface


class AudioParser():
    """ Implements the audio parsing interface for tikplay.

    Parses song metadata, handles database updating, and pushes the audio to soundcard """
    def __init__(self, di=interface.DatabaseInterface):
        self.di = di()
        self.logger = logging.getLogger('AudioParser')

    def find(self, keyword, search_from='filename'):
        """ Find a song from the database based on a certain keyword
        Keyword arguments:
        keyword:
            the keyword to search with
        search_from (optional):
            the column to search from with the keyword, valid values: song_hash, filename, artist, title, length

        Return: true if song exists in database

        """
        pass

    def play(self, keyword, search_from='song_hash'):
        """ Play a song or add it to queue if a song is already playing

        Keyword arguments:
            keyword: the keyword to play
        search_from (optional):
            the column to search for the song_hash with the keyword, valid values:
            song_hash (default), filename, artist, title, length

        Return: true if started playing, false if added to queue

        """
        pass

    def now_playing(self):
        """ Returns the song that is now playing in the format "Artist - Title" """
        pass

    def post_file(self, fp):
        """ Save file to cache and add metadata to database

        Keyword arguments:
            fp: the file to save

        Return: true if successfully saved
        """
        pass


# noinspection PyPep8Naming
class TikplayAPIHandler(http.server.BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.ap = AudioParser()
        http.server.BaseHTTPRequestHandler.__init__(self, *args, **kwargs)

    def do_GET(self):
        path_parts = self.path.split('/')
        if path_parts[1] == 'now_playing':
            self.__get_now_playing()

        elif len(path_parts) < 4:
            self.__get_else(path_parts)

        else:
            self.__error_state()

    def do_POST(self):
        if self.path == '/file':
            self.ap.post_file(self.rfile)

        else:
            self.__error_state()

    def __get_now_playing(self):
        self.send_response(200, 'Now playing: ' + self.ap.now_playing())

    def __get_else(self, path_parts):
        target = path_parts[-1]
        correct_requests = ['song_hash', 'artist', 'title', 'length', 'filename']
        if path_parts[1] == 'find' and path_parts[2] in correct_requests:
            if self.ap.find(target, path_parts[2]):
                self.send_response(302)
            else:
                self.send_response(404)

        elif path_parts[1] == 'play' and path_parts[2] in correct_requests:
            if self.ap.play(target, path_parts[2]):
                self.send_response(200, 'Song is playing')
            else:
                self.send_response(201, 'Song is in the queue')

        else:
            self.__error_state()

    def __error_state(self):
        self.send_response(200, USAGE)


class Server():
    """ Wrapper for HTTPServer and TikplayAPIHandler """
    def __init__(self, host='', port=5000, server_class=http.server.HTTPServer, handler_class=TikplayAPIHandler):
        self.host = host
        self.port = port
        self.server_class = server_class
        self.handler_class = handler_class
        self.__server = self.server_class((self.host, self.port), self.handler_class)
        self.server_thread = threading.Thread(target=self.__server.serve_forever, daemon=True)
        self.logger = logging.getLogger('HTTPServer')

    def start(self):
        """ Start the server and thread """
        self.logger.log(logging.INFO, 'Starting the server')
        self.server_thread.start()

    def stop(self):
        """ Shutdown the server and thread """
        self.logger.log(logging.INFO, 'Stopping the server')
        if self.server_thread.isAlive():
            self.__server.shutdown()
            self.server_thread.join()
            self.logger.log(logging.INFO, 'Stopped')

        else:
            self.logger.log(logging.WARN, 'Already stopped, nothing to do')

    def restart(self):
        """ Unload all the dependencies and stuff from memory, reload and start again """
        # TODO
        pass
