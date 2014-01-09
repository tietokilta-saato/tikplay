#!/usr/bin/env python
# Part of tikplay

import os.path
import subprocess
import urllib.parse
from ..retriever import Retriever


class YouTubeRetriever(Retriever):
    hosts = ["youtube.com", "youtu.be"]

    def __init__(self, conf):
        Retriever.__init__(self, conf)
        self.name = "YouTube"

    def handles(self, url):
        _scheme, netloc, path, params, query, fragment = urllib.parse.urlparse(url)

        # TODO: Metadata checking against DoS via 10-hour videos etc.

        # Strip leading www
        if netloc[:4] == "www.":
            netloc = netloc[4:]

        # http[s]://www.youtube.com/watch?q=12345
        if netloc == "youtube.com":
            if path != "/watch":
                return False
            query = urllib.parse.parse_qs(query)
            if "v" not in query:
                return False
            if not query["v"]:
                return False
            return True

        # http[s]://youtu.be/12345
        elif netloc == "youtu.be":
            return path != "/"

    @staticmethod
    def parse_id(url):
        """Parses the video ID from a YouTube URL"""
        _scheme, netloc, path, params, query, fragment = urllib.parse.urlparse(url)
        netloc = netloc.split(".")

        # http[s]://www.youtube.com/watch?q=12345
        if netloc[-2:] == ["youtube", "com"]:
            if path != "/watch":
                raise ValueError("URL not like youtube.com/watch: " + url)
            query = urllib.parse.parse_qs(query)
            return query["v"][0]

        # http[s]://youtu.be/12345
        elif netloc[-2:] == ["youtu", "be"]:
            return path

        # Something completely different
        else:
            raise ValueError("Unable to parse YouTube URL: " + url)

    def get(self, url):
        video_id = self.parse_id(url)

        # Technically this could be called as pure Python, considering that youtube-dl is a Python program, but
        # this is probably a bit easier.
        # TODO: Is this secure?
        outfile_format = os.path.join(self.conf["download_dir"], "%(id)s.%(ext)s")
        outfile = os.path.join(self.conf["download_dir"], video_id + ".mp3")
        proc = subprocess.Popen(
            ["youtube-dl", "-x", "--audio-format", "mp3", "-o", outfile_format, video_id],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # TODO: Sanity checks for waiting time
        if proc.wait() != 0:
            # TODO: Non-UTF-8 locales
            stdout = proc.stdout.read().decode()
            stderr = proc.stderr.read().decode()
            raise RuntimeError("Nonzero return value from youtube-dl\nstdout:\n{}\nstderr:\n{}".format(stdout, stderr))

        return outfile