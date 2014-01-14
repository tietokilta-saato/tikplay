import logging
import pysoundcard
import pysoundfile
from tikplay.database import interface


class API():
    """ Implements the audio parsing interface for tikplay.

    Parses song metadata, handles database updating, and pushes the audio to soundcard """
    def __init__(self, di=interface.DatabaseInterface):
        self.di = di()
        self.logger = logging.getLogger('AudioParser')

    def find(self, keyword, column='filename'):
        """ Find a song from the database based on a certain keyword
        Keyword arguments:
            keyword: the keyword to search with
            column (optional):
                the column to search from with the keyword, valid values: song_hash, filename, artist, title, length

        Return: true if song exists in database
        """
        return False

    def play(self, song_hash):
        """ Play a song or add it to queue if a song is already playing

        Keyword arguments:
            song_hash: ...

        Return: true if started playing, false if added to queue
        """
        pass

    def store(self, fp):
        """ Save file to cache and add metadata to database

        Keyword arguments:
            fp: the file to save

        Return: true if successfully saved
        """
        return False

    def now_playing(self, queue_length=1):
        """ Shows the now playing or the queue if queue_length is defined

        Keyword arguments:
            queue_length (optional): integer stating the length of queue to return. Default: 1.

        Return: the song that is now playing in the format
            ("Artist - Title"[, "Artist - Title", ...]) or None if empty
        """
        return None
