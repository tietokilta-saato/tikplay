#!/usr/bin/env python
# Part of tikplay

import json
import os.path
import re
import requests
from urllib.parse import urlparse
from tikplay.provider.retriever import Retriever
from tikplay.utils.shell import call_subprocess


class GenericURLRetriever(Retriever):
    """
    A generic URL retriever that tries to guess whether or not the given URL is an audio file and downloads it if it
    seems to be one.
    """

    # Known MIME types for audio files, excluding those starting with "audio/"
    audio_types = [
        "application/ogg",
        "application/octet-stream"
    ]

    def __init__(self, conf):
        super(GenericURLRetriever, self).__init__(conf)
        self.name = "GenericURL"

    def handles(self, url):
        """
        The handler handles everything that seems to be a valid URL.
        """
        scheme, *_rest = urlparse(url)
        return scheme != ""

    @staticmethod
    def is_valid_mime_type(url):
        return url.startswith(("audio/", "video/")) or url in GenericURLRetriever.audio_types

    @staticmethod
    def sanitize(url):
        return re.sub(r'[^a-zA-Z1-9]', '', url)

    def get(self, url):
        req = requests.head(url)
        if req.status_code != 200:
            raise ValueError("Non-200 HTTP response code")
        if not self.is_valid_mime_type(req.headers["content-type"]):
            raise ValueError("Unsupported content type: " + req.headers["content-type"])

        req = requests.get(url)
        download_file = os.path.join(self.conf["download_dir"], "GenericURL-" + self.sanitize(url))
        outfile = os.path.join(self.conf["download_dir"], self.sanitize(url) + ".mp3")
        with open(download_file, "wb") as f:
            f.write(req.content)

        # Check if the file is already an MP3 file
        # TODO: Does sndfile provide an easier method for this?
        proc = call_subprocess("ffprobe", "-v", "quiet", "-show_format", "-of", "json", download_file)
        out = json.loads(proc.stdout.read().decode())
        if out["format"]["format_name"] == "mp3":
            os.rename(download_file, outfile)
            return outfile

        # Convert to MP3
        call_subprocess("ffmpeg", "-i", download_file, "-acodec", "libmp3lame", "-ab", "256k", outfile)
        os.unlink(download_file)
        return outfile