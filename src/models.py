import sqlalchemy as sa
from database import Base


class Song(Base):
    __tablename__ = 'songs'
    song_hash = sa.Column(sa.String(40), primary_key=True)
    filename = sa.Column(sa.Text, nullable=False)
    artist = sa.Column(sa.Text, nullable=True)
    title = sa.Column(sa.Text, nullable=True)
    length = sa.Column(sa.Integer, nullable=True)
    last_played = sa.Column(sa.DateTime, nullable=True)
    play_count = sa.Column(sa.Integer, nullable=False)
