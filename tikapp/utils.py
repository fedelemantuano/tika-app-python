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
import logging
import os
import tempfile
from .exceptions import InvalidParameters, InvalidFilePath


log = logging.getLogger(__name__)


def clean(func):

    def wrapper(*args):
        out, path = func(*args)

        try:
            os.remove(path)
        except OSError:
            pass

        return out

    return wrapper


def file_path(self, file_path=None, payload=None):
    """Given a file path or payload return a file path

    Args:
        file_path (string): path of real file
        payload(string): payload in base64 of file

    Return:
        Path of file
    """

    if payload and not file_path:
        f = write_payload(payload)

    elif file_path and not payload:
        f = file_path

    else:
        msg = "Invalid parameters: you must pass file_path or payload"
        log.exception(msg)
        raise InvalidParameters(msg)

    if not os.path.exists(f):
        msg = "File {!r} does not exist".format(f)
        log.exception(msg)
        raise InvalidFilePath(msg)

    return f


def write_payload(self, payload):
    """Write a base64 payload on temp file

    Args:
        payload (string): payload in base64

    Return:
        Path of file
    """

    temp = tempfile.mkstemp()[1]

    with open(temp, 'wb') as f:
        f.write(payload.decode('base64'))

    return temp
