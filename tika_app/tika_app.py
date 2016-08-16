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
from subprocess import Popen, PIPE, STDOUT

log = logging.getLogger(__name__)


class InvalidTikaAppJar(ValueError):
    pass


class InvalidSwitches(ValueError):
    pass


class TikaApp(object):

    def __init__(
        self,
        file_jar=None
    ):
        if not file_jar or not os.path.exists(file_jar):
            log.exception("Invalid Tika app jar")
            raise InvalidTikaAppJar("Invalid Tika app jar")

        self._file_jar = file_jar

    def _command_template(self, switches):
        """Template for Tika app commands

        Keyword arguments:
        switches -- list of switches to Tika app Jar
        """

        if not isinstance(switches, list):
            log.exception("Invalid switches. Must be a list")
            raise InvalidSwitches("Invalid switches. Must be a list")

        out = Popen(
            [
                "java", "-jar",
                self.file_jar,
                ",".join(switches)
            ],
            stdin=PIPE,
            stdout=PIPE,
            stderr=STDOUT
        )
        return out.communicate()[0]

    @property
    def file_jar(self):
        return self._file_jar

    @property
    def help(self):
        return self._command_template(["--help"])

    def generic(self, switches=["--help"]):
        return self._command_template(switches)


if __name__ == "__main__":
    tika_app = TikaApp(file_jar="/opt/tika/tika-app-1.12.jar")
