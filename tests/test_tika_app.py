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

import os
import sys
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

import tikapp as tika


class TestTikaApp(unittest.TestCase):

    def test_invalid_tika_app_jar(self):
        self.assertRaises(
            tika.InvalidTikaAppJar,
            tika.TikaApp)

    def test_invalid_switches(self):
        tika_app = tika.TikaApp(file_jar="/opt/tika/tika-app-1.13.jar")
        with self.assertRaises(tika.InvalidSwitches):
            tika_app.generic("--help")

    def test_generic(self):
        tika_app = tika.TikaApp(file_jar="/opt/tika/tika-app-1.13.jar")
        self.assertIsInstance(tika_app.generic(), str)

    def test_invalid_parameters(self):
        tika_app = tika.TikaApp(file_jar="/opt/tika/tika-app-1.13.jar")

        with self.assertRaises(tika.InvalidParameters):
            tika_app.extract_all_content(file_path=None, payload=None)

        with self.assertRaises(tika.InvalidParameters):
            tika_app.extract_all_content(file_path=True, payload=True)

    def test_extract_content_from_file(self):
        tika_app = tika.TikaApp(file_jar="/opt/tika/tika-app-1.13.jar")

        self.assertEqual("/opt/tika/tika-app-1.13.jar", tika_app.file_jar)

        result = tika_app.extract_all_content(test_zip)
        self.assertIsInstance(result, str)

        result_obj = json.loads(result)
        self.assertIsInstance(result_obj, list)
        self.assertEqual(len(result_obj), 2)
        self.assertEqual(result_obj[0]["Content-Type"], "application/zip")
        self.assertEqual(
            result_obj[1]["Content-Type"],
            "text/plain; charset=ISO-8859-1")
        self.assertEqual(result_obj[0]["resourceName"], "test.zip")
        self.assertEqual(result_obj[1]["resourceName"], "test.txt")

    def test_extract_content_obj(self):
        tika_app = tika.TikaApp(file_jar="/opt/tika/tika-app-1.13.jar")

        result_obj = tika_app.extract_all_content(
            file_path=test_zip, convert_to_obj=True)

        self.assertIsInstance(result_obj, list)
        self.assertEqual(len(result_obj), 2)
        self.assertEqual(result_obj[0]["Content-Type"], "application/zip")
        self.assertEqual(result_obj[1]["Content-Type"],
                         "text/plain; charset=ISO-8859-1")
        self.assertEqual(result_obj[0]["resourceName"], "test.zip")
        self.assertEqual(result_obj[1]["resourceName"], "test.txt")

    def test_extract_content_from_buffer(self):
        tika_app = tika.TikaApp(file_jar="/opt/tika/tika-app-1.13.jar")

        with open(test_zip, 'rb') as f:
            payload = f.read().encode("base64")

        result_file = tika_app.extract_all_content(file_path=test_zip)
        result_payload = tika_app.extract_all_content(payload=payload)

        self.assertIsInstance(result_file, str)
        self.assertIsInstance(result_payload, str)

        result_file_obj = json.loads(result_file)
        result_payload_obj = json.loads(result_payload)

        self.assertEqual(result_file_obj[0]["Content-Type"],
                         result_payload_obj[0]["Content-Type"])

        self.assertEqual(result_file_obj[1]["Content-Type"],
                         result_payload_obj[1]["Content-Type"])

        self.assertEqual(result_file_obj[1]["resourceName"],
                         result_payload_obj[1]["resourceName"])

    def test_language(self):
        tika_app = tika.TikaApp(file_jar="/opt/tika/tika-app-1.13.jar")
        result = tika_app.detect_language(file_path=test_txt)
        self.assertEqual(result, "en")

    def test_extract_only_content(self):
        tika_app = tika.TikaApp(file_jar="/opt/tika/tika-app-1.13.jar")
        result = tika_app.extract_only_content(file_path=test_txt)
        self.assertIsInstance(result, str)
        self.assertIn("test", result)


if __name__ == '__main__':
    unittest.main()
