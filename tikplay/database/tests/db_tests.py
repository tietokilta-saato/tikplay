import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tikplay.database import Base
from tikplay.database.interface import DatabaseInterface
from tikplay.database.models import Song
from datetime import datetime


SHA1 = u'a' * 40


class DBInterfaceTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine('sqlite:///:memory:', echo=True)
        cls._base = Base
        cls.model = Song

    def setUp(self):
        self._base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()
        self.dbi = DatabaseInterface(self.session, self.model)

    def tearDown(self):
        self._base.metadata.drop_all(self.engine)
        self.session.close()
        del(self.dbi)

    def test_add_song_metadata_full(self):
        self.assertTrue(self.dbi.add_song_metadata(SHA1, 'filename.ext', 'artist', 'title', 0, 1,
                                                   datetime(1970, 1, 2), datetime(1970, 1, 2)))
        self.assertEqual(1, self.session.query(self.model).count())
        query = self.session.query(self.model).one()

        self.assertEqual(SHA1, query.song_hash)
        self.assertEqual('filename.ext', query.filename)
        self.assertEqual('artist', query.artist)
        self.assertEqual('title', query.title)
        self.assertEqual(0, query.length)
        self.assertEqual(1, query.play_count)
        self.assertEqual(datetime(1970, 1, 2), query.date_added)
        self.assertEqual(datetime(1970, 1, 2), query.last_played)

    def test_add_song_metadata_partial(self):
        self.assertTrue(self.dbi.add_song_metadata(SHA1, 'filename.ext'))

        self.assertEqual(1, self.session.query(self.model).count())
        query = self.session.query(self.model).one()

        self.assertEqual(SHA1, query.song_hash)
        self.assertEqual('filename.ext', query.filename)
        self.assertEqual(None, query.artist)
        self.assertEqual(None, query.title)
        self.assertEqual(None, query.length)
        self.assertEqual(0, query.play_count)
        # self.assertEqual(now, query.date_added)  Is not tested since the time doesn't match in millis
        self.assertEqual(None, query.last_played)

    def test_get_song_metadata(self):
        self.test_add_song_metadata_full()
        result = self.dbi.get_song_metadata(SHA1)
        expected = {'song_hash': SHA1,
                    'filename': u'filename.ext',
                    'artist': u'artist',
                    'title': u'title',
                    'length': 0,
                    'play_count': 1,
                    'date_added': datetime(1970, 1, 2),
                    'last_played': datetime(1970, 1, 2)}
        self.assertEqual(expected, result)

    def test_get_song_hashes_by_artist(self):
        self.test_add_song_metadata_full()
        result = self.dbi.get_song_hashes_by_artist('artist')
        expected = [{'song_hash': SHA1,
                    'filename': u'filename.ext',
                    'artist': u'artist',
                    'title': u'title',
                    'length': 0,
                    'play_count': 1,
                    'date_added': datetime(1970, 1, 2),
                    'last_played': datetime(1970, 1, 2)}]
        self.assertEqual(expected, result)

    def test_get_song_hashes_by_filename(self):
        self.test_add_song_metadata_full()
        result = self.dbi.get_song_hashes_by_filename('filename.ext')
        expected = [{'song_hash': SHA1,
                    'filename': u'filename.ext',
                    'artist': u'artist',
                    'title': u'title',
                    'length': 0,
                    'play_count': 1,
                    'date_added': datetime(1970, 1, 2),
                    'last_played': datetime(1970, 1, 2)}]
        self.assertEqual(expected, result)

    def test_get_song_hashes_by_length(self):
        self.test_add_song_metadata_full()
        result = self.dbi.get_song_hashes_by_length(0)
        expected = [{'song_hash': SHA1,
                    'filename': u'filename.ext',
                    'artist': u'artist',
                    'title': u'title',
                    'length': 0,
                    'play_count': 1,
                    'date_added': datetime(1970, 1, 2),
                    'last_played': datetime(1970, 1, 2)}]
        self.assertEqual(expected, result)

    def test_get_song_hashes_by_title(self):
        self.test_add_song_metadata_full()
        result = self.dbi.get_song_hashes_by_title('title')
        expected = [{'song_hash': SHA1,
                    'filename': u'filename.ext',
                    'artist': u'artist',
                    'title': u'title',
                    'length': 0,
                    'play_count': 1,
                    'date_added': datetime(1970, 1, 2),
                    'last_played': datetime(1970, 1, 2)}]
        self.assertEqual(expected, result)

    def test_increment_play_count(self):
        self.test_add_song_metadata_full()
        self.assertTrue(self.dbi.increment_play_count(SHA1))
        query = self.session.query(self.model.play_count).one()
        self.assertEqual(2, query.play_count)

    def test_set_last_played(self):
        self.test_add_song_metadata_full()
        self.assertTrue(self.dbi.set_last_played(SHA1, datetime(2013, 9, 8)))
        query = self.session.query(self.model.last_played).one()
        self.assertEqual(datetime(2013, 9, 8), query.last_played)
