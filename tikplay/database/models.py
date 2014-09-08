import sqlalchemy as sa
from database import Base


class Song(Base):
    __tablename__ = 'songs'
    song_hash = sa.Column(sa.String(40), primary_key=True)
    filename = sa.Column(sa.Text, nullable=False)
    play_count = sa.Column(sa.Integer, nullable=False)
    artist = sa.Column(sa.Text, nullable=True)
    title = sa.Column(sa.Text, nullable=True)
    length = sa.Column(sa.Integer, nullable=True)
    last_played = sa.Column(sa.DateTime, nullable=True)
    date_added = sa.Column(sa.DateTime, nullable=True)

    def __repr__(self):
        return "<Song(song_hash={!r}, filename={!r}, play_count={!r}, artist={!r}, title={!r}, length={!r}, last_played={!r}, date_added={!r})>".format(
               self.song_hash, self.filename, self.play_count, self.artist,
               self.title, self.length, self.last_played, self.date_added)

    def __str__(self):
        return "<Song(song_hash={!s}, filename={!s}, play_count={!s}, artist={!s}, title={!s}, length={!s}, last_played={!s}, date_added={!s})>".format(
               self.song_hash, self.filename, self.play_count, self.artist,
               self.title, self.length, self.last_played, self.date_added)
