import logging
import traceback
from flask import jsonify


def play_file(audio_api, songlogger, fn, filename, user=None):
    """
    Attempts to add the given file to the play queue and log it.
    :param audio_api: The audio API to use
    :param songlogger: The SongLogger instance to use for logging
    :param fn: The filename to play
    :param filename: The original filename of the file (if known) or the URI of the song
    :param user: The user who sent this request, for logging purposes
    :return: flask.Response
    """
    # noinspection PyBroadException
    try:
        result = audio_api.play(fn)
        if result is None:
            return jsonify(error=True, text="Unknown error while playing the song")
        songlogger.write(user, filename)
        return jsonify(error=False, text="OK")
    except Exception as e:
        return jsonify(error=True, text=traceback.format_exc())


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
        self.idle = False
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
                    self.logger.warn("Exception while sending noidle: " + str(e))
                    reconnect = True
            if not reconnect:
                self.player.ping()
        except Exception as e:
            self.logger.warn("Exception while sending ping: " + str(e))
            reconnect = True

        if reconnect:
            self.logger.info("Reconnecting due to the exception above")
            try:
                self.player.close()
            except Exception as e:
                self.logger.warn("Exception while closing connection: " + str(e))
            self.player = self.media_cls.MPDClient()
            self.player.timeout = 3
            self.player.idletimeout = None
            self.player.connect(*self.mpd_addr)

    def play(self, filename):
        """ Play a song or add it to queue if a song is already playing

        Keyword arguments:
            filename: ...

        Return: true if started playing, false if added to queue
        """
        self.logger.info('Playing {}'.format(filename))
        self._check_connection()
        real_song = self.player.search("filename", filename)
        if not real_song:
            return None
        self.player.add(real_song[0]['file'])
        self.player.play()
        self.set_idle()
        return self.now_playing(1)[0]

    def next_(self):
        self._check_connection()

        if len(self.player.playlistinfo()) <= 1:
            self.player.clear()
            res = None
        else:
            self.player.next()
            res = self.now_playing(1)[0]

        self.set_idle()
        return res

    def pause(self):
        self._check_connection()
        self.player.pause()
        res = self.player.status()['state'] == 'pause' or self.player.status()['state'] == 'stop'
        self.set_idle()
        return res

    def resume(self):
        self._check_connection()
        self.player.play()
        res = self.player.status()['state'] == 'play' or self.player.status()['state'] == 'stop'
        self.set_idle()
        return res

    def kill(self):
        self._check_connection()
        self.player.clear()
        res = len(self.player.playlistinfo()) == 0
        self.set_idle()
        return res

    def update(self, directory=None):
        self._check_connection()
        if directory:
            self.player.update(directory)
        else:
            self.player.update()
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
