import unittest
import mock
from tikplay import cache


class CacheTestcase(unittest.TestCase):
    def setup(self):
        self.database_interface = mock.MagicMock()
        self.cache_handler_class = cache.Handler

    def teardown(self):
        pass

    def test_find(self):
        pass

    def test_store(self):
        pass
