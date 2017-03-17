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
import subprocess

import six
from .exceptions import TikaAppJarError
from .utils import file_path, clean, sanitize

try:
    import simplejson as json
except ImportError:
    import json


log = logging.getLogger(__name__)


class TikaApp(object):

    def __init__(self, file_jar=None, memory_allocation=None):
        self.file_jar = file_jar
        self.memory_allocation = memory_allocation

    def __repr__(self):
        class_name = type(self).__name__
        return "{}({!r}, {!r})".format(
            class_name, self.file_jar, self.memory_allocation)

    @property
    def file_jar(self):
        return self._file_jar

    @file_jar.setter
    def file_jar(self, value):
        if not value or not os.path.exists(value):
            msg = "Tika app jar not valid"
            log.exception(msg)
            raise TikaAppJarError(msg)

        self._file_jar = value

    @property
    def memory_allocation(self):
        return self._memory_allocation

    @memory_allocation.setter
    def memory_allocation(self, value):
        self._memory_allocation = value

    @property
    def help(self):
        return self._command_template(["--help"])

    @sanitize
    def _command_template(self, switches):
        """Template for Tika app commands

        Args:
            switches (list): list of switches to Tika app Jar

        Return:
            Standard output data (unicode Python 2, str Python 3)
        """

        command = ["java", "-jar", self.file_jar, "-eUTF-8"]

        if self.memory_allocation:
            command.append("-Xmx{}".format(self.memory_allocation))

        command.extend(switches)

        if six.PY2:
            with open(os.devnull, "w") as devnull:
                out = subprocess.Popen(
                    command, stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE, stderr=devnull)
        elif six.PY3:
            out = subprocess.Popen(
                command, stdin=subprocess.PIPE,
                stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

        stdoutdata, _ = out.communicate()

        return stdoutdata.decode("utf-8").strip()

    def generic(self, switches=["--help"]):
        """Generic method. Default display help"""
        return self._command_template(switches)

    @clean
    def detect_content_type(self, path=None, payload=None):
        """Return the content type of passed file or payload.

        Args:
            path (string): Path of file to analyze
            payload (string): Payload base64 to analyze
        """

        f = file_path(path, payload)
        switches = ["-d", f]
        result = self._command_template(switches).lower()
        return result, path, f

    @clean
    def extract_only_content(self, path=None, payload=None):
        """Return only the text content of passed file

        Args:
            path (string): Path of file to analyze
            payload (string): Payload base64 to analyze
        """

        f = file_path(path, payload)
        switches = ["-t", f]
        result = self._command_template(switches)
        return result, path, f

    @clean
    def detect_language(self, path=None, payload=None):
        """Return the language of passed file or payload.

        Args:
            path (string): Path of file to analyze
            payload (string): Payload base64 to analyze
        """

        f = file_path(path, payload)
        switches = ["-l", f]
        result = self._command_template(switches)
        return result, path, f

    @clean
    def extract_all_content(self, path=None, payload=None,
                            pretty_print=False, convert_to_obj=False):
        """Return a JSON of all contents and metadata of passed file

        Args:
            path (string): Path of file to analyze
            payload (string): Payload base64 to analyze
            pretty_print (boolean): If True adds newlines and whitespace,
                                    for better readability
            convert_to_obj (boolean): If True convert JSON in object
        """
        f = file_path(path, payload)

        if pretty_print:
            switches = ["-J", "-t", "-r", f]
        else:
            switches = ["-J", "-t", f]

        result = self._command_template(switches)

        if result and convert_to_obj:
            result = json.loads(result, encoding="utf-8")

        return result, path, f
