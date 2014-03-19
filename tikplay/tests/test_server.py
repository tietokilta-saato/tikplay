import unittest
import mock
from tikplay import server

class DummyServer():
    def __init__(self, *args, **kwargs):
        self._shutdown = False
        self._alive = False

    def serve_forever(self):
        self._alive = True

        while not self._shutdown:
            if self._shutdown:
                break

        self._alive = False

    def shutdown(self):
        self._shutdown = True

    def is_alive(self):
        return self._alive


class ServerTestcase(unittest.TestCase):
    def setUp(self):
        self.handler_class = mock.MagicMock()
        self.server_class = DummyServer
        self.__server = server.Server(host='127.0.0.1', port=4999,
                                      server_class=self.server_class,
                                      handler_class=self.handler_class)

    def tearDown(self):
        self.handler_class.reset_mock()

    def test_start(self):
        pass

    def test_stop_started(self):
        pass

    def test_restart(self):
        pass

    def test_restart_stopped(self):
        pass


class HandlerTestcase(unittest.TestCase):
    def setup(self):
        pass

    def teardown(self):
        pass
