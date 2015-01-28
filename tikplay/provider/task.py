#!/usr/bin/env python
# Part of tikplay

try:
    import enum
except ImportError:
    import future.enum as enum

import logging
from threading import Thread

# Because PyCharm does not like the functional enum syntax:
# noinspection PyArgumentList
TaskState = enum.Enum('TaskState', 'new running ready done exception')


class Task(Thread):
    """
    Represents the state of a URL retrieval task.
    """
    _next_id = 1

    def __init__(self, uri, retriever, provider):
        Thread.__init__(self)
        self.id = Task._next_id
        Task._next_id += 1
        self.state = TaskState.new
        self.uri = uri
        self.retriever = retriever
        self.provider = provider
        self.filename = None
        self.data = None
        self.daemon = True
        self.exception = None
        self.metadata = {}
        self.log = logging.Logger("Task ({}: {})".format(retriever.name, uri))

    def run(self):
        self.log.debug("Starting task {} ({}), using retriever {}", self.id, self.uri, self.retriever.name)
        try:
            self.state = TaskState.running
            self.filename = self.retriever.get(self.uri)
            self.state = TaskState.ready

        except Exception as e:
            self.log.error("Exception in task %d (%s):", self.id, self.uri)
            self.log.exception(e)
            self.state = TaskState.exception
            self.exception = e
            self.provider.child_exception_queue.put((self, e))