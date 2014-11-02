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
        self.log = logging.getLogger(self.__class__.__name__)

    def get(self, uri):
        """
        Return the audio file from the URI.
        :return: The filename of the downloaded file
        """
        raise NotImplementedError

    def handles_url(self, url):
        """
        Returns whether or not the handler can handle the given URL.
        """
        raise NotImplementedError

    def canonicalize_url(self, url):
        """
        Return a canonical URI for the URL. Raises a ValueError if the handler cannot handle the URL.
        :param url: The URL to canonicalize
        :return: A canonical URI for the URL
        """
        raise NotImplementedError

    def __str__(self):
        return "URL retriever '{}'".format(self.name)