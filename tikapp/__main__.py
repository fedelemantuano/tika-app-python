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

import argparse
import logging
import os
import runpy
import sys

from tikapp import TikaApp

current = os.path.realpath(os.path.dirname(__file__))

__version__ = runpy.run_path(
    os.path.join(current, "version.py"))["__version__"]


def get_args():
    parser = argparse.ArgumentParser(
        description="Wrapper for Apache Tika App.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parsing_group = parser.add_mutually_exclusive_group(required=True)
    parsing_group.add_argument(
        "-f",
        "--file",
        dest="file",
        help="File to submit")
    parsing_group.add_argument(
        "-p",
        "--payload",
        dest="payload",
        help="Base64 payload to submit")
    parsing_group.add_argument(
        "-k",
        "--stdin",
        dest="stdin",
        action="store_true",
        help="Enable parsing from stdin")

    parser.add_argument(
        "-j",
        "--jar",
        dest="jar",
        help="Apache Tika app JAR")

    parser.add_argument(
        "-d",
        "--detect",
        dest="detect",
        action="store_true",
        help="Detect document type")

    parser.add_argument(
        "-t",
        "--text",
        dest="text",
        action="store_true",
        help="Output plain text content")

    parser.add_argument(
        "-l",
        "--language",
        dest="language",
        action="store_true",
        help="Output only language")

    parser.add_argument(
        "-a",
        "--all",
        dest="all",
        action="store_true",
        help="Output metadata and content from all embedded files")

    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version='%(prog)s {}'.format(__version__))

    args = parser.parse_args()

    if args.stdin and args.detect:
        parser.error("Detection content type with file object is not stable.")

    return args


def main():
    args = get_args()

    tika = TikaApp(args.jar or os.environ.get("TIKA_APP_JAR", None))

    parameters = {
        "path": args.file,
        "payload": args.payload,
        "objectInput": sys.stdin if args.stdin else None}

    try:
        if args.detect:
            print(tika.detect_content_type(**parameters))

        if args.text:
            print(tika.extract_only_content(**parameters))

        if args.language:
            print(tika.detect_language(**parameters))

        if args.all:
            parameters["pretty_print"] = True
            print(tika.extract_all_content(**parameters))

    except IOError:
        pass


if __name__ == '__main__':
    logging.getLogger().addHandler(logging.NullHandler())
    main()
