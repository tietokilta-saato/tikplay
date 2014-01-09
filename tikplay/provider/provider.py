#!/usr/bin/env python
# Part of tikplay

import glob
import importlib
import logging
import retrievers
from .retriever import Retriever
from .task import Task

class Provider(object):
    """
    Provides a method for getting the audio data off arbitrary URLs via different retriever modules that can be
    dynamically loaded.
    """

    def __init__(self):
        self.retrievers = {}
        """The list of loaded handlers as a map of name to retriever instance."""
        self.log = logging.Logger("Provider")
        self.register_all()

    def register_all(self):
        """Attempts to automatically register all retrievers in the relevant subdirectory."""
        for name, retriever in retrievers.__dict__.keys():
            if not issubclass(retriever, Retriever): pass
            self.register_retriever(retriever())

    def register_retriever(self, retriever_class):
        """Registers the given retriever, enabling the provider to download audio with the retriever."""

        if not issubclass(retriever_class, Retriever):
            raise TypeError("argument should be a subclass of Retriever")
        instance = retriever_class()
        self.retrievers[instance.name] = instance
        self.retrievers.sort(key = lambda i: i.priority)

    def get(self, url):
        """Retrieves audio from given URL asynchronously. Returns a Task instance."""

        for name, retriever in self.retrievers.items():
            if retriever.handles(url):
                self.log.info("Using handler %s for %s", retriever.name, url)
                try:
                    task = Task(retriever, url)
                    task.start()
                    return task
                except Exception as e:
                    logging.exception()

        logging.warn("No provider found for URL " + url)
        return None