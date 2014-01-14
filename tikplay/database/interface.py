import datetime
from tikplay.database import db
from tikplay.database.models import Song


class DatabaseInterface():
    """ Implements the database interface which abstracts database communication """
    def __init__(self):
        pass

    def add_song_metadata(self, song_hash, filename, artist=None, title=None, length=None, play_count=1,
                          date_added=datetime.datetime.now(), last_played=datetime.datetime.now()):
        """ Stores a new song to database

        Keyword arguments:
            song_hash: SHA-1 hash of the song
            filename: ...
            artist (optional): ...
            title (optional): ...
            length (optional): song length in seconds
            play_count (optional): integer. Default: 1
            date_added (optional): datetime.datetime. Default: datetime.datetime.now()
            last_played (optional): datetime.datetime. Default: datetime.datetime.now()

        Return: true if successfully added
        """
        return False

    def increment_play_count(self, song_hash):
        """ Increments play count with one

        Keyword arguments:
            song_hash: SHA-1 hash of the song

        Return: true if successfully incremented
        """
        return False

    def set_last_played(self, song_hash):
        """ Sets last played to datetime.now()

        Keyword arguments:
            song_hash: SHA-1 hash of the song

        Return: true if successfully set
        """
        return False

    def get_song_metadata(self, song_hash):
        """ Get the song metadata corresponding to the (unique) SHA-1

        Keyword arguments:
            song_hash: ...

        Return: dictionary in the format:
            {'filename': <string>,
             'artist': <string>,
             'title': <string>,
             'length': <string>,
             'play_count': <integer>,
             'date_added': <datetime>,
             'last_played': <datetime>}

             or None if not found
        """
        return None

    def get_song_hashes_by_filename(self, filename):
        """ Get the SHA-1 hashes corresponding to the filename

        Keyword arguments:
            filename: ...

        Return: list of SHA-1 hashes or None if not found
        """
        return None

    def get_song_hashes_by_artist(self, artist):
        """ Get the SHA-1 hashes corresponding to the artist

        Keyword arguments:
            artist: ...

        Return: list of SHA-1 hashes or None if not found
        """
        return None

    def get_song_hashes_by_title(self, title):
        """ Finds the SHA-1 hashes from database corresponding to the title

        Keyword arguments:
            title: (partial) title of the song

        Return: list of SHA-1 hashes or None if not found
        """
        return None

    def get_song_hashes_by_length(self, length):
        """ Get the SHA-1 hash corresponding to the length

        Keyword arguments:
            length: ...

        Return: list of SHA-1 hashes or None if not found
        """
        return None
