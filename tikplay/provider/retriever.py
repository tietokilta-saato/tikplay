#!/usr/bin/env python
# Part of tikplay

import logging


class Retriever(object):
    def __init__(self, conf):
        self.name = "Unnamed retriever"
        """Name of the retriever, eg. YouTube"""

        self.priority = 0
        """Priority of the retriever, smaller number being higher priority"""

        self.conf = conf
        self.log = logging.Logger(self.name)

    def handles(self, url):
        """Returns whether or not the retriever can handle the given URL."""
        raise NotImplementedError

    def get(self, url):
        """Return the audio file from the URL."""
        raise NotImplementedError

    def __str__(self):
        return "URL retriever '{}'".format(self.name)