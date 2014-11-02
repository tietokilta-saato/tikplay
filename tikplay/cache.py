import logging
import os
import os.path


class Cache:
    def __init__(self, directory):
        self.dir = os.path.expanduser(directory)
        self.log = logging.getLogger('AudioCache')

        if not os.path.exists(self.dir):
            self.log.info("Cache directory does not exist, creating")
            os.makedirs(self.dir)

    def get_song(self, uri):
        """
        :param uri: URI specifying the song to find
        :return: The filename relative to the cache directory or None
        """
        service, id_ = uri.split(":", 1)
        id_ = self.sanitize(id_)

        fn = os.path.join(self.dir, service, id_) + ".mp3"
        if os.path.exists(fn):
            self.log.debug("%s was found in the cache", fn)
            return os.path.join(service, id_)

        self.log.debug("%s was not found in the cache", fn)
        return None

    @staticmethod
    def sanitize(id_):
        """
        Sanitize the given ID so it contains no characters not allowed in filenames.
        :param id_: The ID to sanitize
        :return: The sanitized ID
        """
        return id_.replace("/", "_").replace("~", "_")

    def move_song(self, uri, fn):
        """
        Moves the song in `fn` to the correct location as specified by the URI.
        :param uri: URI specifying the song
        :param fn: The current location of the file
        :return: The new filename of the song
        """

        service, id_ = uri.split(":", 1)
        id_ = self.sanitize(id_)
        service_dir = os.path.join(self.dir, service)
        if not os.path.exists(service_dir):
            self.log.info("Cache directory for %s does not exist, creating", service)
            os.mkdir(service_dir)

        new_fn = os.path.join(service_dir, id_) + ".mp3"  # A small hack so mpd reads the file despite the actual format
        os.rename(os.path.expanduser(fn), os.path.expanduser(new_fn))
        return os.path.join(service, id_)