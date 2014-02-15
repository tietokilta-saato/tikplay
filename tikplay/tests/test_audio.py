import unittest
import mock
from tikplay import audio


class AudioTestcase(unittest.TestCase):
    def setUp(self):
        self.media_class = mock.MagicMock()
        self.player = mock.MagicMock()
        self.audio_api_class = audio.API(media_player=self.player, media=self.media_class)

    def tearDown(self):
        self.media_class.reset_mock()
        self.player.reset_mock()

    def test_play_successful(self):
        pass

    def test_play_queued(self):
        pass

    def test_now_playing(self):
        pass
