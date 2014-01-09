#!/usr/bin/env python
# Part of tikplay

import logging
from threading import Thread

class Task(Thread):
    """
    Represents the state of a URL retrieval task.
    """

    def __init__(self, url, retriever):
        Thread.__init__(self)
        self.state = None
        self.url = url
        self.retriever = retriever
        self.data = None
        self.daemon = True
        self.log = logging.Logger("Task ({}: {})".format(retriever.name, url))

    def run(self):
        self.retriever.get(self.url)