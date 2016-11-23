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
from subprocess import Popen, PIPE, STDOUT
from .exceptions import \
    InvalidTikaAppJar, \
    InvalidSwitches, \
    InvalidFilePath, \
    InvalidParameters, \
    TempIOError

try:
    import simplejson as json
except ImportError:
    import json

log = logging.getLogger(__name__)


class TikaApp(object):

    def __init__(
        self,
        file_jar=None,
        memory_allocation=None
    ):

        self.file_jar = file_jar
        self.memory_allocation = memory_allocation

    def _write_payload(self, payload):
        """Write a base64 payload on temp file

        Keyyyword arguments:
        payload -- payload in base64
        """

        try:
            temp = tempfile.mkstemp()[1]
            with open(temp, 'wb') as f:
                f.write(payload.decode('base64'))
            return temp
        except:
            log.exception("Failed opening '{}' file".format(temp))
            raise TempIOError("Failed opening '{}' file".format(temp))

    def _file_path(self, file_path=None, payload=None):
        """Check if parameters are corrects and return file path

        Keyword arguments:
        file_path -- path of real file
        payload -- payload in base64 of file
        """

        if payload and not file_path:
            file_ = self._write_payload(payload)
        elif file_path and not payload:
            file_ = file_path
        else:
            log.exception(
                "Invalid parameters: you must pass file_path or payload")
            raise InvalidParameters(
                "Invalid parameters: you must pass file_path or payload")

        if not os.path.exists(file_):
            log.exception("File {} does not exist".format(file_))
            raise InvalidFilePath("File {} does not exist".format(file_))

        return file_

    def _command_template(self, switches):
        """Template for Tika app commands

        Keyword arguments:
        switches -- list of switches to Tika app Jar
        """

        if not isinstance(switches, list):
            log.exception("Invalid switches. Must be a list")
            raise InvalidSwitches("Invalid switches. Must be a list")

        if self.memory_allocation:
            command = [
                "java",
                "-Xmx{}".format(self.memory_allocation),
                "-jar",
                self.file_jar,
            ]
        else:
            command = [
                "java",
                "-jar",
                self.file_jar,
            ]
        command.extend(switches)

        out = Popen(
            command,
            stdin=PIPE,
            stdout=PIPE,
            stderr=STDOUT
        )
        return out.communicate()[0].strip()

    @property
    def file_jar(self):
        return self._file_jar

    @file_jar.setter
    def file_jar(self, value):
        if not value or not os.path.exists(value):
            log.exception("Invalid Tika app jar")
            raise InvalidTikaAppJar("Invalid Tika app jar")

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

    def generic(self, switches=["--help"]):
        """Generic method. Default display help"""
        return self._command_template(switches)

    def detect_content_type(self, file_path=None, payload=None):
        """Return the content type of passed file or payload.

        Keyword arguments:
        file_path -- Path of file
        payload -- Payload base64 of file
        """

        file_ = self._file_path(file_path, payload)

        switches = [
            "-d",
            file_,
        ]

        result = self._command_template(switches).lower()

        if payload:
            os.remove(file_)

        return result

    def extract_only_content(self, file_path=None, payload=None):
        """Return only the text content of passed file

        Keyword arguments:
        file_path -- Path of file
        payload -- Payload base64 of file
        """

        file_ = self._file_path(file_path, payload)

        switches = [
            "-t",
            file_,
        ]

        result = self._command_template(switches).strip()

        if payload:
            os.remove(file_)

        return result

    def detect_language(self, file_path=None, payload=None):
        """Return the language of passed file or payload.

        Keyword arguments:
        file_path -- Path of file
        payload -- Payload base64 of file
        """

        file_ = self._file_path(file_path, payload)

        switches = [
            "-l",
            file_,
        ]

        result = self._command_template(switches)

        if payload:
            os.remove(file_)

        return result

    def extract_all_content(
        self,
        file_path=None,
        payload=None,
        pretty_print=False,
        convert_to_obj=False,
    ):
        """Return a JSON of all contents and metadata of passed file

        Keyword arguments:
        file_path -- Path of file
        payload -- Payload base64 of file
        pretty_print -- If True adds newlines and whitespace,
                        for better readability
        convert_to_obj -- If True convert JSON in object
        """

        file_ = self._file_path(file_path, payload)

        if pretty_print:
            switches = [
                "-J",
                "-t",
                "-r",
                file_,
            ]
        else:
            switches = [
                "-J",
                "-t",
                file_,
            ]

        result = self._command_template(switches)
        if result and convert_to_obj:
            result = json.loads(result)

        if payload:
            os.remove(file_)

        return result
