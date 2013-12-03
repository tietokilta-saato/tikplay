from statics import USAGE
import database_interface
import datetime
import pysoundcard
import pysoundfile
import BaseHTTPServer
import SocketServer


class Server():
    """ Implements the socket interface for tikplay and listens on a certain port """
    def __init__(self, host='', port=5000):
        self.host = host
        self.port = port

    def start(self):
        pass

    def stop(self):
        pass

    def restart(self):
        pass


class TIKPlayAPIHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.ap = AudioParser()
        BaseHTTPServer.BaseHTTPRequestHandler.__init__(*args, **kwargs)

    def do_GET(self):
        if '/hash/' in self.path and self.path.startswith('/play/'):
            pass

        elif '/hash/' in self.path and self.path.startswith('/find/'):
            pass

        elif '/name/' in self.path and self.path.startswith('/play'):
            pass

        elif '/name/' in self.path and self.path.startswith('/find/'):
            pass

        elif self.path == '/now_playing':
            pass

        else:
            self.__error_state()

    def do_POST(self):
        if self.path == '/file':
            pass

        else:
            self.__error_state()

    def __error_state(self):
        self.send_response(418, USAGE)


class AudioParser():
    """ Implements the audio parsing interface for tikplay.

    Parses song metadata, handles database updating, and pushes the audio to soundcard """
    def __init__(self):
        self.di = database_interface.DatabaseInterface()

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

    def play(self, song_hash):
        """ Play a song or add it to queue if a song is already playing

        Keyword arguments:
            song_hash: the identifier to with which to select the file to play

        Return: true if started playing, false if added to queue

        """
        pass

    def now_playing(self):
        """ Returns the song that is now playing in the format "Artist - Title" """
        pass

    def POST_file(self, fp):
        """ Save file to cache and add metadata to database

        Keyword arguments:
            fp: the file to save, should be in the format that socket.recv() returns

        Return: true if successfully saved
        """
        pass
