import datetime


class DatabaseInterface():
    """ Implements the database interface which abstracts database communication """
    def __init__(self, db, model):
        self.db = db
        self.model = model

    def add_song_metadata(self, song_hash, filename, artist=None, title=None, length=None, play_count=0,
                          date_added=datetime.datetime.now(), last_played=None):
        """ Stores a new song to database

        Keyword arguments:
            song_hash: SHA-1 hash of the song
            filename: ...
            artist (optional): ...
            title (optional): ...
            length (optional): song length in seconds
            play_count (optional): integer. Default: 0
            date_added (optional): datetime.datetime. Default: datetime.datetime.now()
            last_played (optional): datetime.datetime. Default: None

        Return: true if successfully added
        """
        new_song = self.model(song_hash=song_hash, filename=filename, artist=artist, title=title, length=length,
                              play_count=play_count, last_played=last_played, date_added=date_added)
        self.db.add(new_song)
        self.db.commit()
        return True

    def increment_play_count(self, song_hash):
        """ Increments play count with one

        Keyword arguments:
            song_hash: SHA-1 hash of the song

        Return: true if successfully incremented
        """
        query = self.db.query(self.model).filter(self.model.song_hash == song_hash)
        _song = query.one()
        _song.play_count += 1
        self.db.add(_song)
        self.db.commit()
        return True

    def set_last_played(self, song_hash, date=datetime.datetime.now()):
        """ Sets last played to date

        Keyword arguments:
            song_hash: SHA-1 hash of the song
            date (optional): defaults to datetime.datetime.now()

        Return: true if successfully set
        """
        query = self.db.query(self.model).filter(self.model.song_hash == song_hash)
        _song = query.one()
        _song.last_played = date
        self.db.add(_song)
        self.db.flush()
        return True

    def get_song_metadata(self, song_hash):
        """ Get the song metadata corresponding to the (unique) SHA-1

        Keyword arguments:
            song_hash: ...

        Return: dictionary in the format:
            {'song_hash': <string:40>,
             'filename': <string>,
             'artist': <string>,
             'title': <string>,
             'length': <string>,
             'play_count': <integer>,
             'date_added': <datetime>,
             'last_played': <datetime>}

             or None if not found
        """
        query = self.db.query(self.model).filter(self.model.song_hash == song_hash)
        return query.one().as_dict()

    def get_song_hashes_by_filename(self, filename):
        """ Get the SHA-1 hashes corresponding to the filename

        Keyword arguments:
            filename: ...

        Return: List of song metadata dictionaries or None if not found
        """
        filename = filename.replace('*', '%')
        query = self.db.query(self.model).filter(self.model.filename.like(filename)).order_by(self.model.last_played)
        if query.count() == 0:
            return None

        return [_.as_dict() for _ in query]

    def get_song_hashes_by_artist(self, artist):
        """ Get the SHA-1 hashes corresponding to the artist

        Keyword arguments:
            artist: ...

        Return: List of song metadata dictionaries or None if not found
        """
        artist = artist.replace('*', '%')
        query = self.db.query(self.model).filter(self.model.artist.like(artist)).order_by(self.model.last_played)
        if query.count() == 0:
            return None

        return [_.as_dict() for _ in query]

    def get_song_hashes_by_title(self, title):
        """ Finds the SHA-1 hashes from database corresponding to the title

        Keyword arguments:
            title: (partial) title of the song

        Return: List of song metadata dictionaries or None if not found
        """
        title = title.replace('*', '%')
        query = self.db.query(self.model).filter(self.model.title.like(title)).order_by(self.model.last_played)
        if query.count() == 0:
            return None

        return [_.as_dict() for _ in query]

    def get_song_hashes_by_length(self, length):
        """ Get the SHA-1 hash corresponding to the length

        Keyword arguments:
            length: ...

        Return: List of song metadata dictionaries or None if not found
        """
        query = self.db.query(self.model).filter(self.model.length == length).order_by(self.model.last_played)
        if query.count() == 0:
            return None

        return [_.as_dict() for _ in query]
