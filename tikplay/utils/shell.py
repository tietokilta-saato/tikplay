#!/usr/bin/env python
# Part of tikplay

import subprocess


def call_subprocess(*params):
    """
    Calls a subprocess, raises a RuntimeError if the subprocess fails and returns the subprocess.Popen instance.
    Parameters:
        Use as if giving a list to subprocess.Popen(), ie. call_subprocess("ls", "-l")
    """
    proc = subprocess.Popen(params, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if proc.wait() != 0:
        stdout = proc.stdout.read().decode()
        stderr = proc.stderr.read().decode()
        raise RuntimeError("Nonzero return value from subprocess\nstdout:\n{}\nstderr:\n{}".format(stdout, stderr))

    return proc