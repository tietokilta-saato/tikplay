import logging


class API():
    """ Implements the audio parsing interface for tikplay.

    Parses song metadata, handles database updating, and pushes the audio to soundcard

    Also implements basic song metadata fetching from the database
    """
    def __init__(self, media_cls, mpd_addr):
        self.logger = logging.getLogger('AudioAPI')
        self.logger.info('Connecting to MPD')
        self.media_cls = media_cls
        self.player = media_cls.MPDClient()
        self.player.timeout = 3
        self.player.idletimeout = None
        self.player.connect(*mpd_addr)
        self.mpd_addr = mpd_addr
        self.player.consume(1)
        self.player.repeat(0)
        self.player.setvol(100)
        self.player.single(0)
        self.logger.info('Connected')
        self.set_idle()

    def set_idle(self):
        self.player.send_idle()
        self.idle = True

    def _check_connection(self):
        reconnect = False
        try:
            if self.idle:
                try:
                    self.player.noidle()
                except Exception as e:
                    self.logger.warn("Exception: " + str(e))
                    reconnect = True
            self.player.ping()
        except Exception as e:
            self.logger.warn("Exception: " + str(e))
            reconnect = True

        if reconnect:
            self.player.close()
            self.player = self.media_cls.MPDClient()
            self.player.timeout = 3
            self.player.idletimeout = None
            self.player.connect(*self.mpd_addr)
            self.set_idle()

    def play(self, filename):
        """ Play a song or add it to queue if a song is already playing

        Keyword arguments:
            filename: ...

        Return: true if started playing, false if added to queue
        """
        self.logger.info('Playing {}'.format(filename))
        self._check_connection()
        self.player.update()
        real_song = self.player.search("filename", filename)
        if not real_song:
            return None
        self.player.add(real_song[0]['file'])
        self.player.play()
        self.set_idle()
        return self.now_playing(1)[0]

    def next_(self):
        self._check_connection()
        self.player.next()
        self.set_idle()

    def pause(self):
        self._check_connection()
        self.player.pause()
        self.set_idle()

    def resume(self):
        self._check_connection()
        self.player.play()
        self.set_idle()

    def kill(self):
        self._check_connection()
        self.player.clear()
        self.set_idle()

    def now_playing(self, queue_length=10):
        """ Shows the now playing or the queue if queue_length is defined

        Keyword arguments:
            queue_length (optional): integer stating the length of queue to return. Default: 1.

        Return: the song that is now playing in the MPD format
        """
        self._check_connection()
        res = self.player.playlistinfo()[:queue_length]
        self.set_idle()
        return res
