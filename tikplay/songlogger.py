#!/usr/bin/env python
# Part of tikplay

import datetime
import os.path


class SongLogger:
    def __init__(self, fn):
        self.fp = open(os.path.expanduser(fn), "ab")

    def write(self, user, song):
        line = "{0:%Y}-{0:%m}-{0:%d}T{0:%H}:{0:%M}:{0:%S}Z {1} {2}\n".format(
            datetime.datetime.utcnow(), user, song
        )
        self.fp.write(line.encode('utf8', error='backslashreplace'))
        self.fp.flush()