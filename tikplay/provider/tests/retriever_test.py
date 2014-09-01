#!/usr/bin/env python
# Part of tikplay
# Yes, this is a bit of a non-test.

from nose.tools import *
from tikplay.provider.retriever import Retriever

class TestRetriever(object):
    def __init__(self):
        self.retriever = Retriever({})

    @raises(NotImplementedError)
    def test_handles(self):
        self.retriever.handles("")

    @raises(NotImplementedError)
    def test_get(self):
        self.retriever.get("")

    def test_str(self):
        assert str(self.retriever) == "URL retriever 'Unnamed retriever'"