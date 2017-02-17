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

import base64
import os
import sys
import six
import unittest

try:
    import simplejson as json
except ImportError:
    import json

unittest_path = os.path.realpath(os.path.dirname(__file__))
root = os.path.join(unittest_path, '..')
sys.path.append(root)
test_txt = os.path.join(unittest_path, 'files', 'test.txt')
test_zip = os.path.join(unittest_path, 'files', 'test.zip')

TIKA_JAR = "/opt/tika/tika-app-1.14.jar"

import tikapp as tika
from tikapp.exceptions import TikaAppJarError, FilePathError


class TestTikaApp(unittest.TestCase):

    def test_tikaappjarerror(self):
        with self.assertRaises(TikaAppJarError):
            tika.TikaApp()

    def test_filepatherror(self):
        tika_app = tika.TikaApp(file_jar=TIKA_JAR)

        with self.assertRaises(TypeError):
            tika_app.extract_all_content(path=None, payload=None)

        with self.assertRaises(FilePathError):
            tika_app.extract_all_content(
                path="/tmp/fake_rand_file", payload=None)

    def test_generic(self):
        tika_app = tika.TikaApp(file_jar=TIKA_JAR)
        self.assertIsInstance(tika_app.generic(), six.text_type)

    def test_extract_all_content_file(self):
        tika_app = tika.TikaApp(file_jar=TIKA_JAR)

        self.assertEqual(TIKA_JAR, tika_app.file_jar)

        result = tika_app.extract_all_content(test_zip)
        self.assertIsInstance(result, six.text_type)

        result_obj = json.loads(result, encoding="utf-8")
        self.assertIsInstance(result_obj, list)
        self.assertEqual(len(result_obj), 2)
        self.assertEqual(result_obj[0]["Content-Type"], "application/zip")
        self.assertEqual(
            result_obj[1]["Content-Type"],
            "text/plain; charset=ISO-8859-1")
        self.assertEqual(result_obj[0]["resourceName"], "test.zip")
        self.assertEqual(result_obj[1]["resourceName"], "test.txt")

    def test_extract_all_content_file_obj(self):
        tika_app = tika.TikaApp(file_jar=TIKA_JAR)

        result_obj = tika_app.extract_all_content(
            path=test_zip, convert_to_obj=True)

        self.assertIsInstance(result_obj, list)
        self.assertEqual(len(result_obj), 2)
        self.assertEqual(result_obj[0]["Content-Type"], "application/zip")
        self.assertEqual(result_obj[1]["Content-Type"],
                         "text/plain; charset=ISO-8859-1")
        self.assertEqual(result_obj[0]["resourceName"], "test.zip")
        self.assertEqual(result_obj[1]["resourceName"], "test.txt")

    def test_extract_all_content_buffer(self):
        tika_app = tika.TikaApp(file_jar=TIKA_JAR)

        with open(test_zip, 'rb') as f:
            payload = base64.b64encode(f.read())

        result_file = tika_app.extract_all_content(path=test_zip)
        result_payload = tika_app.extract_all_content(payload=payload)

        self.assertIsInstance(result_file, six.text_type)
        self.assertIsInstance(result_payload, six.text_type)

        result_file_obj = json.loads(result_file, encoding="utf-8")
        result_payload_obj = json.loads(result_payload, encoding="utf-8")

        self.assertEqual(result_file_obj[0]["Content-Type"],
                         result_payload_obj[0]["Content-Type"])

        self.assertEqual(result_file_obj[1]["Content-Type"],
                         result_payload_obj[1]["Content-Type"])

        self.assertEqual(result_file_obj[1]["resourceName"],
                         result_payload_obj[1]["resourceName"])

    def test_detect_language(self):
        tika_app = tika.TikaApp(file_jar=TIKA_JAR)
        result = tika_app.detect_language(path=test_txt)
        self.assertEqual(result, "en")

    def test_extract_only_content(self):
        tika_app = tika.TikaApp(file_jar=TIKA_JAR)
        result = tika_app.extract_only_content(path=test_txt)
        self.assertIsInstance(result, six.text_type)
        self.assertIn("test", result)


if __name__ == '__main__':
    unittest.main(verbosity=2)
