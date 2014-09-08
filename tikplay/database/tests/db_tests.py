import unittest
import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from tikplay.database import interface
from datetime import datetime


SHA1 = 'a' * 40


class DBInterfaceTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine('sqlite:///:memory:', echo=True)
        _base = declarative_base()

        class _Song(_base):
            __tablename__ = 'test_songs'
            song_hash = sa.Column(sa.String(40), primary_key=True)
            filename = sa.Column(sa.Text, nullable=False)
            play_count = sa.Column(sa.Integer, nullable=False)
            artist = sa.Column(sa.Text, nullable=True)
            title = sa.Column(sa.Text, nullable=True)
            length = sa.Column(sa.Integer, nullable=True)
            last_played = sa.Column(sa.DateTime, nullable=True)
            date_added = sa.Column(sa.DateTime, nullable=True)

        cls.model = _Song

    def setUp(self):
        self.model.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()
        self.dbi = interface(self.session, self.model)

    def tearDown(self):
        self.model.drop(self.engine, checkfirst=True)
        self.session.close()
        del(self.dbi)

    def test_add_song_metadata_full(self):
        self.assertTrue(self.dbi.add_song_metadata(SHA1, 'filename.ext', 'artist', 'title', 0, 0,
                                                   datetime(1970, 1, 1), datetime(1970, 1, 1)))

        self.assertEqual(1, self.session.query(self.model).count())
        self.assertEqual(SHA1, self.session.query(self.model.song_hash).all()[0])
        self.assertEqual('filename.ext', self.session.query(self.model.filename).all()[0])
        self.assertEqual('artist', self.session.query(self.model.artist).all()[0])
        self.assertEqual('title', self.session.query(self.model.title).all()[0])
        self.assertEqual(0, self.session.query(self.model.length).all()[0])
        self.assertEqual(0, self.session.query(self.model.play_count).all()[0])
        self.assertEqual(0, self.session.query(self.model.date_added).all()[0])
        self.assertEqual(0, self.session.query(self.model.last_played).all()[0])

    def test_add_song_metadata_partial(self):
        now = datetime.datetime.now()
        self.assertTrue(self.dbi.add_song_metadata(SHA1, 'filename.ext'))

        self.assertEqual(1, self.session.query(self.model).count())
        self.assertEqual(SHA1, self.session.query(self.model.song_hash).all()[0])
        self.assertEqual('filename.ext', self.session.query(self.model.filename).all()[0])
        self.assertEqual(None, self.session.query(self.model.artist).all()[0])
        self.assertEqual(None, self.session.query(self.model.title).all()[0])
        self.assertEqual(None, self.session.query(self.model.length).all()[0])
        self.assertEqual(1, self.session.query(self.model.play_count).all()[0])
        self.assertEqual(now, self.session.query(self.model.date_added).all()[0])
        self.assertEqual(now, self.session.query(self.model.last_played).all()[0])

    def test_get_song_metadata(self):
        self.test_add_song_metadata_full()
        result = self.dbi.get_song_metadata()
        expected = {'filename': 'filename.ext',
                    'artist': 'artist',
                    'title': 'title',
                    'length': 0,
                    'play_count': 0,
                    'date_added': datetime(1970, 1, 1),
                    'last_played': datetime(1970, 1, 1)}
        self.assertEqual(expected, result)

    def test_get_song_hashes_by_artist(self):
        self.test_add_song_metadata_full()
        result = self.dbi.get_song_hashes_by_artist('artist')
        expected = [SHA1]
        self.assertEqual(expected, result)

    def test_get_song_hashes_by_filename(self):
        self.test_add_song_metadata_full()
        result = self.dbi.get_song_hashes_by_filename('filename.ext')
        expected = [SHA1]
        self.assertEqual(expected, result)

    def test_get_song_hashes_by_length(self):
        self.test_add_song_metadata_full()
        result = self.dbi.get_song_hashes_by_length(0)
        expected = [SHA1]
        self.assertEqual(expected, result)

    def test_get_song_hashes_by_title(self):
        self.test_add_song_metadata_full()
        result = self.dbi.get_song_hashes_by_title('title')
        expected = [SHA1]
        self.assertEqual(expected, result)

    def test_increment_play_count(self):
        self.test_add_song_metadata_full()
        self.assertTrue(self.dbi.increment_play_count(SHA1))
        self.assertEqual(1, self.session.query(self.model.play_count).all()[0])

    def test_set_last_played(self):
        self.test_add_song_metadata_full()
        self.assertTrue(self.dbi.set_last_played(SHA1, datetime(2013, 9, 8)))
        self.assertEqual(datetime(2013, 9, 8), self.session.query(self.model.last_played).all()[0])
