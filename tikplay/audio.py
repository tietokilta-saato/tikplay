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
        self.player.timeout = None
        self.player.idletimeout = None
        self.player.connect(*mpd_addr)
        self.player.consume(1)
        self.player.repeat(0)
        self.player.setvol(100)
        self.player.single(0)
        self.logger.info('Connected')
        self.player.send_idle()
        self.idle = True

    def _toggle_idle(self):
        if self.idle:
            self.player.noidle()
            self.idle = False
        else:
            self.player.send_idle()
            self.idle = True

    def play(self, filename):
        """ Play a song or add it to queue if a song is already playing

        Keyword arguments:
            filename: ...

        Return: true if started playing, false if added to queue
        """
        self.logger.info('Playing {}'.format(filename))
        self._toggle_idle()
        self.player.update()
        self.player.add(filename)
        self.player.play()
        self._toggle_idle()
        return self.now_playing(1)[0]

    def next_(self):
        self._toggle_idle()
        self.player.next()
        self._toggle_idle()

    def pause(self):
        self._toggle_idle()
        self.player.pause()
        self._toggle_idle()

    def resume(self):
        self._toggle_idle()
        self.player.play()
        self._toggle_idle()

    def kill(self):
        self._toggle_idle()
        self.player.clear()
        self._toggle_idle()

    def now_playing(self, queue_length=10):
        """ Shows the now playing or the queue if queue_length is defined

        Keyword arguments:
            queue_length (optional): integer stating the length of queue to return. Default: 1.

        Return: the song that is now playing in the MPD format
        """
        self._toggle_idle()
        res = self.player.playlistinfo()[:queue_length]
        self._toggle_idle()
        return res
