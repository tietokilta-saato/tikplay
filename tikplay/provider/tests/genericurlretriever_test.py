#!/usr/bin/env python
# Part of tikplay

import json
import os.path
import tempfile
from nose.tools import *
from tikplay.provider.retrievers.generic_url import GenericURLRetriever
from tikplay.utils.shell import call_subprocess


class TestGenericURLRetriever(object):
    def __init__(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.conf = {"download_dir": self.tmpdir.name}
        self.retriever = GenericURLRetriever(self.conf)

    def test_handles(self):
        assert self.retriever.handles_url("https://archive.org/download/testmp3testfile/mpthreetest.mp3")
        assert not self.retriever.handles_url("not a url")

    def test_download_non_mp3(self):
        """
        Test downloading a known non-MP3 file that should be converted before using.
        """
        fn = self.retriever.get("url:http://upload.wikimedia.org/wikipedia/commons/c/c8/Example.ogg")
        assert os.path.exists(fn)
        proc = call_subprocess("ffprobe", "-v", "quiet", "-show_format", "-of", "json", fn)
        fmt = json.loads(proc.stdout.read().decode())
        assert fmt["format"]["format_name"] == "mp3"

    def test_download_mp3(self):
        """
        Test downloading a known MP3 file.
        """
        fn = self.retriever.get("url:https://ia700200.us.archive.org/1/items/testmp3testfile/mpthreetest.mp3")
        assert os.path.exists(fn)
        proc = call_subprocess("ffprobe", "-v", "quiet", "-show_format", "-of", "json", fn)
        fmt = json.loads(proc.stdout.read().decode())
        assert fmt["format"]["format_name"] == "mp3"

    @raises(ValueError)
    def test_404_url(self):
        self.retriever.get("http://google.com/error")

    @raises(ValueError)
    def test_invalid_content_type(self):
        self.retriever.get("http://humanstxt.org/humans.txt")

TestGenericURLRetriever.test_download_non_mp3.slow = 1
TestGenericURLRetriever.test_download_mp3.slow = 1