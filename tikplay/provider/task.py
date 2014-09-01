#!/usr/bin/env python
# Part of tikplay

import logging
from threading import Thread


class Task(Thread):
    """
    Represents the state of a URL retrieval task.
    """

    def __init__(self, url, retriever, provider):
        Thread.__init__(self)
        self.state = None
        self.url = url
        self.retriever = retriever
        self.provider = provider
        self.data = None
        self.daemon = True
        self.log = logging.Logger("Task ({}: {})".format(retriever.name, url))

    def run(self):
        try:
            self.retriever.get(self.url)
        except Exception as e:
            self.state = "exception" # TODO: enum
            self.provider.child_exception_queue.put((self, e))