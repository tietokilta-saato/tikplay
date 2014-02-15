import logging
import pyglet


class API():
    """ Implements the audio parsing interface for tikplay.

    Parses song metadata, handles database updating, and pushes the audio to soundcard

    Also implements basic song metadata fetching from the database
    """
    def __init__(self, media_player=pyglet.media.Player, media=pyglet.media):
        self.player = media_player()
        self.media = media
        self.logger = logging.getLogger('AudioAPI')

    def play(self, song_hash):
        """ Play a song or add it to queue if a song is already playing

        Keyword arguments:
            song_hash: ...

        Return: true if started playing, false if added to queue
        """
        audio_file = self.media.load(song_hash)
        self.player.queue(audio_file)
        if not self.player.playing:
            self.player.play()

        return self.player.source == audio_file

    def next(self):
        self.player.next_source()

    def pause(self):
        self.player.pause()

    def resume(self):
        self.player.resume()

    def kill(self):
        while self.player.playing:
            self.player.next_source()

    def now_playing(self, queue_length=1):
        """ Shows the now playing or the queue if queue_length is defined

        Keyword arguments:
            queue_length (optional): integer stating the length of queue to return. Default: 1.

        Return: the song that is now playing in the format
            [(Artist, Title), (Artist, Title), ...) or None if empty
        """
        src = self.player.source

        return [(src.info.author, src.info.title)]
