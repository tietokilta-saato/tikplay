#!/usr/bin/env python
# Part of tikplay

import importlib
import logging
import queue
from inspect import isclass
import provider.retrievers as retrievers
from .retriever import Retriever
from .task import Task


class Provider(object):
    """
    Provides a method for getting the audio data off arbitrary URLs via different retriever modules that can be
    dynamically loaded.
    """

    def __init__(self, conf, register_all=True):
        self.retrievers = []
        """The list of loaded handlers."""
        self.child_exception_queue = queue.Queue()
        """A list of tuples (task, exception) used by the child threads for reporting exceptions."""
        self.conf = conf
        self.log = logging.Logger("Provider")
        if register_all:
            self.register_all()

    def register_all(self):
        """Attempts to automatically register all retrievers in the relevant subdirectory."""
        for module in retrievers.__all__:
            module = importlib.import_module('provider.retrievers.' + module)
            for name, retriever in module.__dict__.items():
                # Discard non-classes
                if not isclass(retriever):
                    continue
                # Discard the abstract Retriever class that is imported in the module
                if retriever is Retriever:
                    continue
                # Discard non-Retrievers
                if not issubclass(retriever, Retriever):
                    continue
                self.log.info("Registering retriever %s.%s", module.__name__, name)
                self.register_retriever(retriever)

    def register_retriever(self, retriever_class):
        """Registers the given retriever, enabling the provider to download audio with the retriever."""
        if not issubclass(retriever_class, Retriever):
            raise TypeError("argument should be a subclass of Retriever")
        instance = retriever_class(self.conf)
        self.retrievers.append(instance)
        self.retrievers.sort(key=lambda i: i.priority)

    def canonicalize(self, url):
        """Canonicalizes the given URL, returning a suitable URI"""
        for retriever in self.retrievers:
            if retriever.handles_url(url):
                return retriever.canonicalize_url(url)

        raise ValueError("No provider found, cannot canonicalize " + url)

    def get(self, uri):
        """Retrieves audio from the given URI asynchronously. Returns a Task instance."""
        service, id_ = uri.split(":", 1)
        for retriever in self.retrievers:
            if retriever.__class__.uri_service == service:
                self.log.info("Using handler %s for %s", retriever.name, uri)
                task = Task(uri, retriever, self)
                task.start()
                return task

        logging.warning("No provider found for URI " + uri)
        raise ValueError("No provider found for URI " + uri)

    def has_exception(self):
        """Returns whether or not there are unhandled exceptions in the child exception queue."""
        return not self.child_exception_queue.empty()

    def get_exceptions(self):
        """Returns all unhandled child exceptions as a list of dicts {task: Task, exception: Exception}."""
        ret = []
        while True:
            try:
                ret.append(dict(zip(("task", "exception"), self.child_exception_queue.get_nowait())))
            except queue.Empty:
                return ret