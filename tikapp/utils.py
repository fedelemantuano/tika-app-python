#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright 2016 Fedele Mantuano (https://twitter.com/fedelemantuano)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from __future__ import unicode_literals
import base64
import logging
import os
import tempfile
from unicodedata import normalize
from exceptions import TikaAppFilePathError


log = logging.getLogger(__name__)


def sanitize(func):
    """ NFC is the normalization form recommended by W3C. """

    def wrapper(*args, **kwargs):
        return normalize('NFC', func(*args, **kwargs))
    return wrapper


def clean(func):
    """
    This decorator removes the temp file from disk. This is the case where
    you want to analyze from a payload.
    """
    def wrapper(*args, **kwargs):
        # tuple: output command, path given from command line,
        # path of templ file when you give the payload
        out, given_path, path = func(*args, **kwargs)

        try:
            if not given_path:
                os.remove(path)
        except OSError:
            pass

        return out

    return wrapper


def file_path(path=None, payload=None, objectInput=None):
    """
    Given a file path, payload or file object, it writes file on disk and
    returns the temp path.

    Args:
        path (string): path of real file
        payload(string): payload in base64 of file
        objectInput (object): file object/standard input to analyze

    Returns:
        Path of file
    """
    f = path if path else write_payload(payload, objectInput)

    if not os.path.exists(f):
        msg = "File {!r} does not exist".format(f)
        log.exception(msg)
        raise TikaAppFilePathError(msg)

    return f


def write_payload(payload=None, objectInput=None):
    """
    This function writes a base64 payload or file object on disk.

    Args:
        payload (string): payload in base64
        objectInput (object): file object/standard input to analyze

    Returns:
        Path of file
    """

    temp = tempfile.mkstemp()[1]
    log.debug("Write payload in temp file {!r}".format(temp))

    with open(temp, 'wb') as f:
        if payload:
            payload = base64.b64decode(payload)
        elif objectInput:
            payload = objectInput.read()

        f.write(payload)

    return temp
