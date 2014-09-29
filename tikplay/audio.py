import logging


class API():
    """ Implements the audio parsing interface for tikplay.

    Parses song metadata, handles database updating, and pushes the audio to soundcard

    Also implements basic song metadata fetching from the database
    """
    def __init__(self, media_cls, mpd_addr):
        self.logger = logging.getLogger('AudioAPI')
        self.logger.info('Connecting to MPD')
        self.player = media_cls.MPDClient()
        self.player.timeout = 10
        self.player.idletimeout = None
        self.player.connect(*mpd_addr)
        self.player.consume(1)
        self.player.repeat(0)
        self.player.setvol(100)
        self.player.single(0)
        self.logger.info('Connected')
        self.player.send_idle()

    def play(self, filename):
        """ Play a song or add it to queue if a song is already playing

        Keyword arguments:
            filename: ...

        Return: true if started playing, false if added to queue
        """
        self.logger.info('Playing {}'.format(filename))
        self.player.noidle()
        self.player.update()
        self.player.add(filename)
        self.player.play()
        self.player.send_idle()

    def next_(self):
        self.player.noidle()
        self.player.next()
        self.player.send_idle()

    def pause(self):
        self.player.noidle()
        self.player.pause()
        self.player.send_idle()

    def resume(self):
        self.player.noidle()
        self.player.play()
        self.player.send_idle()

    def kill(self):
        self.player.noidle()
        self.player.clear()
        self.player.send_idle()

    def now_playing(self, queue_length=10):
        """ Shows the now playing or the queue if queue_length is defined

        Keyword arguments:
            queue_length (optional): integer stating the length of queue to return. Default: 1.

        Return: the song that is now playing in the MPD format
        """
        self.player.noidle()
        res = self.player.playlistinfo()[:queue_length]
        self.player.send_idle()
        return res
