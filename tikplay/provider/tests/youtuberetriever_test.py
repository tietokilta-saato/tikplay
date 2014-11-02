#!/usr/bin/env python
# Part of tikplay

import os.path
import tempfile
from nose.tools import *
from youtube_dl import DownloadError
from tikplay.provider.retrievers.youtube import YouTubeRetriever


class TestYouTubeRetriever(object):
    def __init__(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.conf = {"download_dir": self.tmpdir.name}
        self.retriever = YouTubeRetriever(self.conf)

    def test_handles(self):
        """Tests the handling of different valid and invalid URLs."""
        assert self.retriever.handles_url("http://www.youtube.com/watch?v=oHg5SJYRHA0")
        assert self.retriever.handles_url("https://www.youtube.com/watch?v=oHg5SJYRHA0")
        assert self.retriever.handles_url("http://youtu.be/oHg5SJYRHA0")
        assert self.retriever.handles_url("https://youtu.be/oHg5SJYRHA0")
        assert not self.retriever.handles_url("http://www.youtube.com")
        assert not self.retriever.handles_url("http://www.youtube.com/watch")
        assert not self.retriever.handles_url("http://www.youtube.com/watch?v=")
        assert not self.retriever.handles_url("http://www.youtube.com/watch?x=12345")
        assert not self.retriever.handles_url("https://youtu.be/")
        assert not self.retriever.handles_url("http://google.com")

    def test_parse_id(self):
        """Tests that video IDs are parsed correctly."""
        assert self.retriever.parse_id("http://www.youtube.com/watch?v=oHg5SJYRHA0") == "oHg5SJYRHA0"
        assert self.retriever.parse_id("http://youtu.be/oHg5SJYRHA0") == "oHg5SJYRHA0"

    @raises(ValueError)
    def test_parse_invalid_domain(self):
        """Tests parsing an invalid domain."""
        self.retriever.parse_id("http://google.com")

    @raises(ValueError)
    def test_parse_id_invalid_path(self):
        """Tests parsing an invalid path in youtube.com."""
        self.retriever.parse_id("http://youtube.com/help")

    @raises(DownloadError)
    def test_get_invalid_id(self):
        """Tests retrieving a non-existent video ID, which should lead to youtube-dl returning an error."""
        self.retriever.get("http://www.youtube.com/watch?v=invalid")

    def test_download(self):
        """Tests that downloading a video actually works and that the download path is predictable."""
        fn = self.retriever.get("http://www.youtube.com/watch?v=oHg5SJYRHA0")
        assert fn == os.path.join(self.tmpdir.name, "oHg5SJYRHA0.mp3")

TestYouTubeRetriever.test_download.slow = 1