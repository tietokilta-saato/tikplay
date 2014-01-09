#!/usr/bin/env python
# A generic configuration module that uses JSON as its backend format.

import json


class Configuration:
    """
        A configuration object that works like a dict and automatically
        updates changes to the disk.
    """

    def __init__(self, filename, ignore_errors=True):
        """
            @param filename: The filename of the configuration file
            @param ignore_errors: Whether to ignore missing keys and return
                None for them, or to properly raise a KeyError.
        """
        self.ignore_errors = bool(ignore_errors)
        self.filename = filename
        self.data = {}
        self.read()

    def read(self):
        """
            Reloads the configuration from disk.
        """
        f = open(self.filename)
        self.data = json.load(f)
        f.close()

    def write(self):
        """
            Writes the configuration as JSON to the defined filename
        """
        f = open(self.filename, "w")
        json.dump(self.data, f, indent=4)
        f.close()

    # dict emulation methods
    def __len__(self):
        return len(self.data)

    def __getitem__(self, key):
        if self.ignore_errors:
            return self.data.get(key, None)
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value
        self.write()

    def __delitem__(self, key):
        if self.ignore_errors and key not in self.data:
            return
        del self.data[key]

    def __iter__(self):
        return iter(self.data)

    def __contains__(self, key):
        return key in self.data

    def keys(self):
        return self.data.keys()

    def items(self):
        return self.data.items()

    def get(self, key, default):
        return self.data.get(key, default)