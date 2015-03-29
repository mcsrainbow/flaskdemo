#!/bin/env python

'''
A simple interface to execute shell commands.
Reference: fabric/operations.py.

Examples:
    >>> from operations import local

    >>> out = local('uname -r')
    >>> print out
    2.6.32
    >>> print out.stdout
    2.6.32
    >>> print out.failed
    False
    >>> print out.succeeded
    True
'''

import subprocess

class _AttributeString(str):
    """
    Simple string subclass to allow arbitrary attribute access.
    """
    @property
    def stdout(self):
        return str(self)

def local(cmd, capture=True, shell=None):
    out_stream = subprocess.PIPE
    err_stream = subprocess.PIPE
    p = subprocess.Popen(cmd, shell=True, stdout=out_stream, stderr=err_stream, executable=shell)
    (stdout, stderr) = p.communicate()

    out = _AttributeString(stdout.strip() if stdout else "")
    err = _AttributeString(stderr.strip() if stderr else "")

    out.cmd = cmd
    out.failed = False
    out.return_code = p.returncode
    out.stderr = err
    if out.return_code != 0:
        out.failed = True
    out.succeeded = not out.failed

    return out
