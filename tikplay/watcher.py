#!/usr/bin/env python
# Part of tikplay

import logging
from threading import Thread
import time

from provider.task import TaskState


class TaskWatcher(Thread):
    """
    Watches the task dict for asynchronous download tasks that are complete, then moves them to the correct directory
    and adds them to the play queue.
    """
    def __init__(self, task_dict, cache, audio_api, songlogger):
        Thread.__init__(self)
        self.log = logging.getLogger("TaskWatcher")
        self.daemon = True
        self.tasks = task_dict
        self.cache = cache
        self.audio_api = audio_api
        self.songlogger = songlogger

    def run(self):
        self.log.info("Task watcher running")
        while True:
            time.sleep(3)
            for id_, task in self.tasks.items():
                if task.state == TaskState.ready:
                    self.log.info("Task %d (%s) is done, handling", task.id, task.uri)
                    if task.filename is None:
                        self.log.warn("Task %d (%s) is ready but has no filename!", task.id, task.uri)
                        task.state = TaskState.exception
                        continue

                    new_fn = self.cache.move_song(task.uri, task.filename)
                    self.log.debug("Task %d (%s) moved to cache, %s", task.id, task.uri, new_fn)

                    # A small hack, preferrably use mpd's auto_update instead of this
                    # This delay is acceptable as tasks only are run when the file is not in the cache
                    self.audio_api.update(task.uri.split(":", 1)[0])
                    time.sleep(2.0)

                    try:
                        result = self.audio_api.play(new_fn)
                        self.songlogger.write(task.metadata.get("user"),
                                              task.metadata.get("original_filename", task.uri))
                        if result is None:
                            task.state = TaskState.exception
                        else:
                            task.state = TaskState.done
                    except Exception as e:
                        self.log.exception(e)
                        task.state = TaskState.exception