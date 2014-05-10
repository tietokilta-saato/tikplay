import json
import logging
import os
import random
from database import interface


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

    def store(self, fp, filename=None):
        """ Save file to cache and add metadata to database

        Keyword arguments:
            fp: the file to save

        Return: filepath to the saved file if successful, False otherwise
        """
        ## TODO: make cache folder configurable
        self.logger.debug('Trying to store a new file')
        cache_dir = os.path.expanduser('~/.tikplay_cache')
        filepath = ""
        if not os.path.exists(cache_dir):
            try:
                os.mkdir(cache_dir)
            except IOError:
                self.logger.warn('Could not create cache directory')
                return False

        if filename:
            filepath = os.path.join(cache_dir, filename)
            with open(filepath, 'wb') as _file:
                _file.write(fp.read())

        else:
            random_id = int(random.random() * 100000.0)  # 100 000 should be enough buffer for unique songs
            filepath = os.path.join(cache_dir, random_id)
            with open(filepath, 'wb') as _file:
                _file.write(fp.read())

        self.logger.info('Wrote a new file to: %s', filepath)
        ## TODO: update file info to the database
        return filepath
