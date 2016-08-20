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
from tika_app.tika_app import TikaApp
import magic
import os
import timeit

profiling_path = os.path.realpath(os.path.dirname(__file__))
test_zip = os.path.join(profiling_path, "lorem_ipsum.txt.zip")
test_txt = os.path.join(profiling_path, "lorem_ipsum.txt")


def tika_content_type():
    tika_client = TikaApp(
        file_jar="/opt/tika/tika-app-1.13.jar"
    )

    output = tika_client.detect_content_type(
        file_path=test_zip,
    )

    return output


def tika_detect_language():
    tika_client = TikaApp(
        file_jar="/opt/tika/tika-app-1.13.jar"
    )

    output = tika_client.detect_language(
        file_path=test_zip,
    )

    return output


def magic_content_type():
    mime = magic.Magic(mime=True)
    output = mime.from_file(test_zip)
    return output


def tika_extract_all_content(memory=None):
    tika_client = TikaApp(
        file_jar="/opt/tika/tika-app-1.13.jar",
        memory_allocation=memory,
    )

    output = tika_client.extract_all_content(
        file_path=test_zip,
    )

    return output


def tika_extract_only_content(memory=None):
    tika_client = TikaApp(
        file_jar="/opt/tika/tika-app-1.13.jar",
        memory_allocation=memory,
    )

    output = tika_client.extract_only_content(
        file_path=test_zip,
    )

    return output


if __name__ == "__main__":
    """Results:

    tika_content_type()             0.708108 sec
    tika_detect_language()          1.748900 sec
    magic_content_type()            0.000215 sec
    tika_extract_all_content()      0.849755 sec
    tika_extract_only_content()     0.791735 sec
    """

    repeats = 15
    functions = [
        "tika_content_type",
        "tika_detect_language",
        "magic_content_type",
        "tika_extract_all_content",
        "tika_extract_only_content",
    ]

    for function in functions:
        t = timeit.Timer(
            "{0}()".format(function),
            "from __main__ import {0}".format(function),
        )
        sec = t.timeit(repeats) / repeats

        print("{function}()\t\t{sec:.6f} sec".format(**locals()))
