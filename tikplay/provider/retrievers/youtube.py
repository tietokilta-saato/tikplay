#!/usr/bin/env python
# Part of tikplay

import os.path
import urllib.parse
import youtube_dl
from ..retriever import Retriever


class YouTubeRetriever(Retriever):
    uri_service = "yt"

    def __init__(self, conf):
        Retriever.__init__(self, conf)
        self.name = "YouTube"

    def canonicalize_url(self, url):
        if not self.handles_url(url):
            raise ValueError("Invalid YouTube URL: " + url)
        return "yt:" + self.parse_id(url)

    def handles_url(self, url):
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
            # parse_qs ensures that empty values are not in the returned dict, making testing for them unnecessary
            if "v" not in query:
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
            # path contains the leading slash
            return path[1:]

        # Something completely different
        else:
            raise ValueError("Unable to parse YouTube URL: " + url)

    def get(self, uri):
        video_id = uri.split(":")[1]
        outfile = os.path.join(self.conf["download_dir"], video_id + ".mp3")

        ydl_opts = {
            "logger": self.log,
            "outtmpl": os.path.join(self.conf["download_dir"], "%(id)s.%(ext)s")
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.add_post_processor(youtube_dl.FFmpegExtractAudioPP(
                preferredcodec="mp3",
                preferredquality="4"
            ))
            ydl.add_post_processor(youtube_dl.FFmpegMetadataPP())
            ydl.download([video_id])
        return outfile