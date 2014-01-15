import unittest
import mock
from tikplay import server


class ServerTestcase(unittest.TestCase):
    def setUp(self):
        self.handler_class = mock.MagicMock()
        self.server_class = mock.MagicMock()
        self.server_class.serve_forever = mock.MagicMock()
        self.server = server.Server(host='127.0.0.1', port=4999,
                                      server_class=self.server_class, handler_class=self.handler_class)

    def tearDown(self):
        self.handler_class.reset_mock()
        self.server_class.reset_mock()

    def test_start(self):
        self.server.start()
        assert self.server_class.return_value.serve_forever.called
        assert self.server.server_thread.isAlive()

    def test_stop_stopped(self):
        assert not self.server.server_thread.isAlive()
        self.server.stop()
        assert not self.server_class.return_value.shutdown.called

    def test_stop_started(self):
        self.server.start()
        assert self.server.server_thread.isAlive()
        self.server.stop()
        assert self.server_class.return_value.shutdown.called

    def test_restart(self):
        pass


class HandlerTestcase(unittest.TestCase):
    def setup(self):
        pass

    def teardown(self):
        pass


class AudioTestcase(unittest.TestCase):
    def setup(self):
        pass

    def teardown(self):
        pass
