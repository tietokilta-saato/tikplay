from database import db
from database.models import Song


class DatabaseInterface():
    """ Implements the database interface which abstracts database communication """
    def __init__(self):
        pass

    def store_new_song(self, song_hash, filename, artist=None, title=None, length=None):
        """ Stores a new song to database

        Keyword arguments:
            song_hash: SHA-1 hash of the song
            filename: ...
            artist: ...
            title: ...
            length: song length in seconds

        Return: true if successfully added
        """
        pass

    def increment_play_count(self, song_hash):
        """ Increments play count with one

        Keyword arguments:
            song_hash: SHA-1 hash of the song

        Return: true if successfully incremented
        """
        pass

    def set_last_played(self, song_hash):
        """ Sets last played to datetime.now()

        Keyword arguments:
            song_hash: SHA-1 hash of the song

        Return: true if successfully set
        """
        pass

    def find_song_hash(self, partial_title):
        """ Finds the song hash from database

        Keyword arguments:
            partial_title: (partial) title of the song

        Return: list of SHA-1 hash strings
        """
        pass

    def find_last_played(self, partial_title):
        """ Finds the last played date from database

        Keyword arguments:
            partial_title: (partial) title of the song

        Return: list of (SHA-1, Datetime) objects
        """
        pass

    def find_play_count(self, partial_title):
        """ Finds the play count from database

        Keyword arguments:
            partial_title: (partial) title of the song

        Return: list of (SHA-1, integer) objects
        """
        pass

    def get_song_hash_by_filename(self, filename):
        """ Get the SHA-1 hash corresponding to the filename

        Keyword arguments:
            filename: ...

        Return: list of SHA-1 hashes
        """
        pass

    def get_song_hash_by_artist(self, artist):
        """ Get the SHA-1 hash corresponding to the artist

        Keyword arguments:
            artist: ...

        Return: list of SHA-1 hashes
        """
        pass

    def get_song_hash_by_title(self, title):
        """ Get the SHA-1 hash corresponding to the title

        Keyword arguments:
            title: ...

        Return: list of SHA-1 hashes
        """
        pass

    def get_song_hash_by_length(self, length):
        """ Get the SHA-1 hash corresponding to the length

        Keyword arguments:
            length: ...

        Return: list of SHA-1 hashes
        """
        pass

    def get_filename(self, song_hash):
        """ Get the filename according to the (unique) SHA-1 hash

        Keyword arguments:
            song_hash: ...

        Return: string
        """
        pass

    def get_artist(self, song_hash):
        """ Get the artist according to the (unique) SHA-1 hash

        Keyword arguments:
            song_hash: ...

        Return: string
        """
        pass

    def get_title(self, song_hash):
        """ Get the title according to the (unique) SHA-1 hash

        Keyword arguments:
            song_hash: ...

        Return: string
        """
        pass

    def get_length(self, song_hash):
        """ Get the length according to the (unique) SHA-1 hash

        Keyword arguments:
            song_hash: ...

        Return: string
        """
        pass

    def get_last_played(self, song_hash):
        """ Get the last played date according to the (unique) SHA-1 hash

        Keyword arguments:
            song_hash: ...

        Return: Datetime object
        """
        pass

    def get_play_count(self, song_hash):
        """ Get the last played date according to the (unique) SHA-1 hash

        Keyword arguments:
            song_hash: ...

        Return: Integer
        """
        pass
