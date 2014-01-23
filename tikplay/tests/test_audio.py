import unittest
import mock
from tikplay import audio


class AudioTestcase(unittest.TestCase):
    def setup(self):
        self.database_interface = mock.MagicMock()
        self.audio_api_class = audio.API

    def teardown(self):
        pass

    def test_play(self):
        pass

    def test_now_playing(self):
        pass
