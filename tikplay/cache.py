import logging
import pysoundfile
from tikplay.database import interface


class Handler():
    def __init__(self, di=interface.DatabaseInterface):
        self.di = di()
        self.logger = logging.getLogger('AudioCache')

    def find(self, keyword, column='filename'):
        """ Find a song from the database based on a certain keyword
        Keyword arguments:
            keyword: the keyword to search with
            column (optional):
                the column to search from with the keyword, valid values: song_hash, filename, artist, title, length

        Return: The data that exists in the database in JSON format or None

        Raise: KeyError if unknown column
        """
        if column == 'song_hash':
            return self.__find_with_method(keyword, self.di.get_song_metadata)

        elif column == 'filename':
            return self.__find_with_method(keyword, self.di.get_song_hashes_by_filename)

        elif column == 'artist':
            return self.__find_with_method(keyword, self.di.get_song_hashes_by_artist)

        elif column == 'title':
            return self.__find_with_method(keyword, self.di.get_song_hashes_by_title)

        elif column == 'length':
            return self.__find_with_method(keyword, self.di.get_song_hashes_by_length)

        else:
            self.logger.warn('Tried finding "%s" unknown column: %s', (keyword, column))
            raise KeyError('Unknown column')

    def __find_with_method(self, keyword, method):
        self.logger.info('Finding %s from database with method %s', (keyword, method))
        data = method(keyword)
        if data:
            return json.dumps(data)

        else:
            return None

    def store(self, fp):
        """ Save file to cache and add metadata to database

        Keyword arguments:
            fp: the file to save

        Return: true if successfully saved
        """
        return False
