#!/usr/bin/env python
# Part of tikplay

import json
import os.path
import re
import requests
from provider.retriever import Retriever
from utils import is_url
from utils.shell import call_subprocess


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
    uri_service = "url"

    def __init__(self, conf):
        super(GenericURLRetriever, self).__init__(conf)
        self.name = "GenericURL"
        self.priority = 9001  # This is a generic handler, so we want a low priority for it (big = lower priority)

    def handles_url(self, url):
        return is_url(url)

    def canonicalize_url(self, url):
        if not self.handles_url(url):
            raise ValueError("Invalid URL: " + url)
        # This is a bit icky, but practically good enough.
        return "url:" + url

    @staticmethod
    def is_valid_mime_type(url):
        return url.startswith(("audio/", "video/")) or url in GenericURLRetriever.audio_types

    @staticmethod
    def sanitize(url):
        return re.sub(r'[^a-zA-Z1-9]', '', url)

    def get(self, uri):
        _, url = uri.split(":", 1)
        self.log.debug("Getting URL " + url)
        req = requests.head(url)
        if req.status_code != 200:
            self.log.warning("Non-200 return code from %s", url)
            raise ValueError("Non-200 HTTP response code")
        if not self.is_valid_mime_type(req.headers["content-type"]):
            self.log.warning("Invalid MIME type from %s: %s", url, req.headers["content-type"])
            raise ValueError("Unsupported content type: " + req.headers["content-type"])

        req = requests.get(url)
        download_file = os.path.join(os.path.expanduser(self.conf["download_dir"]), "GenericURL-" + self.sanitize(url))
        outfile = os.path.join(os.path.expanduser(self.conf["download_dir"]), self.sanitize(url) + ".mp3")
        with open(download_file, "wb") as f:
            f.write(req.content)

        # Check if the file is already an MP3 file
        # TODO: Does sndfile provide an easier method for this?
        proc = call_subprocess("ffprobe", "-v", "quiet", "-show_format", "-of", "json", download_file)
        out = json.loads(proc.stdout.read().decode())
        if out["format"]["format_name"] == "mp3":
            self.log.debug("File is already an MP3, renaming to %s", outfile)
            os.rename(download_file, outfile)
            return outfile

        # Convert to MP3
        self.log.debug("Converting file to MP3")
        call_subprocess("ffmpeg", "-i", download_file, "-acodec", "libmp3lame", "-ab", "256k", outfile)
        os.unlink(download_file)
        return outfile