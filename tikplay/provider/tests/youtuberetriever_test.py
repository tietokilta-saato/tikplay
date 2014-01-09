#!/usr/bin/env python
# Part of tikplay

import os.path
import tempfile
from tikplay.provider.retrievers.youtube import YouTubeRetriever


class TestYouTubeRetriever(object):
    def __init__(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.conf = {"download_dir": self.tmpdir.name}
        self.retriever = YouTubeRetriever(self.conf)

    def test_handles(self):
        assert self.retriever.handles("http://www.youtube.com/watch?v=oHg5SJYRHA0")
        assert self.retriever.handles("https://www.youtube.com/watch?v=oHg5SJYRHA0")
        assert self.retriever.handles("http://youtu.be/oHg5SJYRHA0")
        assert self.retriever.handles("https://youtu.be/oHg5SJYRHA0")
        assert not self.retriever.handles("http://www.youtube.com")
        assert not self.retriever.handles("http://www.youtube.com/watch")
        assert not self.retriever.handles("http://www.youtube.com/watch?v=")
        assert not self.retriever.handles("http://www.youtube.com/watch?x=12345")
        assert not self.retriever.handles("https://youtu.be/")
        assert not self.retriever.handles("http://google.com")

    def test_download(self):
        fn = self.retriever.get("http://www.youtube.com/watch?v=oHg5SJYRHA0")
        assert fn == os.path.join(self.tmpdir.name, "oHg5SJYRHA0.mp3")