#!/usr/bin/env python
# Part of tikplay

from nose.tools import *
import tikplay.provider.retrievers
import tikplay.provider.retrievers.youtube
from tikplay.provider.provider import Provider
from tikplay.provider.retriever import Retriever
from tikplay.provider.task import Task


class MockRetriever(Retriever):
    """
    A Retriever that handles everything and only returns the given URL from get() and sets test flags in TestProvider.
    """
    uri_service = "mock"

    def __init__(self, conf):
        super(MockRetriever, self).__init__(conf)
        TestProvider.retriever_initialized = True

    def get(self, url):
        TestProvider.get_called = True
        return url


class ErrorRetriever(Retriever):
    """
    A Retriever that handles everything but raises a NotImplementedError whenever get() is called.
    """
    uri_service = "error"

    def __init__(self, conf):
        super(ErrorRetriever, self).__init__(conf)

    def handles_url(self, url):
        return True

    def get(self, url):
        raise NotImplementedError


class NonRetrieverClass(object):
    """
    A dummy class used for testing.
    """
    pass


class MockModule(object):
    """
    Fakes a module file, to be injected into tikplay.provider.retrievers for testing non-Retriever classes in
    Provider.register_all()
    """

    def __init__(self):
        self.__dict__ = {"not_a_retriever": NonRetrieverClass}


class TestProvider(object):
    retriever_initialized = False
    get_called = False

    def __init__(self):
        self.provider = Provider({}, False)
        self.retriever_initialized = False
        self.handles_called = False
        self.get_called = False

    @staticmethod
    def setUp():
        TestProvider.retriever_initialized = False
        TestProvider.handles_called = False
        TestProvider.get_called = False

    @staticmethod
    def tearDown():
        TestProvider.retriever_initialized = False
        TestProvider.handles_called = False
        TestProvider.get_called = False

    @raises(ValueError)
    def test_no_retriever(self):
        """Tests getting something from Provider when there are no retrievers registered."""
        self.provider.get("x:y")

    @raises(TypeError)
    def test_register_invalid_retriever(self):
        """Tests registering a non-Retriever class as a retriever."""
        self.provider.register_retriever(str)

    def test_mock_provider(self):
        """A simple functional test for the general flow of the Provider."""
        self.provider.register_retriever(MockRetriever)
        assert len(self.provider.retrievers) == 1
        assert isinstance(self.provider.get("mock:http://example.com"), Task)
        assert TestProvider.retriever_initialized
        assert TestProvider.get_called

    def test_error_provider(self):
        """Tests the child thread exception handling in Provider."""
        self.provider.register_retriever(ErrorRetriever)
        task = self.provider.get("error:error")
        assert self.provider.has_exception()
        exceptions = self.provider.get_exceptions()
        assert len(exceptions) == 1
        assert exceptions[0]["task"] is task
        assert isinstance(exceptions[0]["exception"], NotImplementedError)

    def test_register_all_zero(self):
        """Tests Provider.register_all() with no valid retrievers visible."""
        tikplay.provider.retrievers.__all__ = []
        self.provider.register_all()
        assert len(self.provider.retrievers) == 0
