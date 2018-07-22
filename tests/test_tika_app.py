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
import logging
import os
import six
import unittest

import mailparser
import simplejson as json

from context import TikaApp, TikaAppJarError, TikaAppFilePathError


unittest_path = os.path.realpath(os.path.dirname(__file__))
test_txt = os.path.join(unittest_path, 'files', 'test.txt')
test_zip = os.path.join(unittest_path, 'files', 'test.zip')
test_pdf = os.path.join(unittest_path, 'files', 'pdf1.pdf')
mail_test_1 = os.path.join(unittest_path, 'files', 'mail_test_1')
TIKA_APP_JAR = os.environ.get(
    "TIKA_APP_JAR", None) or "/opt/tika/tika-app-1.18.jar"


class TestTikaApp(unittest.TestCase):

    def setUp(self):
        self.parser = mailparser.parse_from_file(mail_test_1)
        self.tika = TikaApp(file_jar=TIKA_APP_JAR)

    def test_JSONDecodeError(self):
        for i in self.parser.attachments:

            r = self.tika.extract_all_content(
                payload=i["payload"], convert_to_obj=False)
            self.assertIsInstance(r, six.text_type)

            r = self.tika.extract_all_content(
                payload=i["payload"], convert_to_obj=True)
            self.assertIsInstance(r, list)

    def test_tikaappjarerror(self):
        with self.assertRaises(TikaAppJarError):
            TikaApp()

    def test_filepatherror(self):
        with self.assertRaises(TypeError):
            self.tika.extract_all_content(path=None, payload=None)

        with self.assertRaises(TikaAppFilePathError):
            self.tika.extract_all_content(
                path="/tmp/fake_rand_file", payload=None)

    def test_generic(self):
        self.assertIsInstance(self.tika.generic(), six.text_type)

    def test_extract_all_content_file(self):
        self.maxDiff = None
        self.assertEqual(TIKA_APP_JAR, self.tika.file_jar)

        result = self.tika.extract_all_content(test_zip)
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

        result = self.tika.extract_all_content(test_zip, convert_to_obj=True)
        with open(test_zip) as f:
            result_stdin = self.tika.extract_all_content(
                objectInput=f, convert_to_obj=True)
            self.assertEqual(
                result[0]["X-TIKA:content"],
                result_stdin[0]["X-TIKA:content"])

    def test_extract_all_content_file_obj(self):
        result_obj = self.tika.extract_all_content(
            path=test_zip, convert_to_obj=True)

        self.assertIsInstance(result_obj, list)
        self.assertEqual(len(result_obj), 2)
        self.assertEqual(result_obj[0]["Content-Type"], "application/zip")
        self.assertEqual(result_obj[1]["Content-Type"],
                         "text/plain; charset=ISO-8859-1")
        self.assertEqual(result_obj[0]["resourceName"], "test.zip")
        self.assertEqual(result_obj[1]["resourceName"], "test.txt")

    def test_extract_all_content_buffer(self):
        with open(test_zip, 'rb') as f:
            payload = base64.b64encode(f.read())

        result_file = self.tika.extract_all_content(path=test_zip)
        result_payload = self.tika.extract_all_content(payload=payload)

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
        result = self.tika.detect_language(path=test_txt)
        self.assertEqual(result, "en")

        with open(test_txt) as f:
            result_stdin = self.tika.detect_language(objectInput=f)
            self.assertEqual(result, result_stdin)

    def test_detect_content_type(self):
        result = self.tika.detect_content_type(path=test_zip)
        self.assertEqual(result, "application/zip")

        with open(test_zip) as f:
            result_stdin = self.tika.detect_content_type(objectInput=f)
            self.assertEqual(result, result_stdin)

        result = self.tika.detect_content_type(path=test_txt)
        self.assertEqual(result, "text/plain")

        with open(test_txt) as f:
            result_stdin = self.tika.detect_content_type(objectInput=f)
            self.assertEqual(result, result_stdin)

    def test_extract_only_content(self):
        result = self.tika.extract_only_content(path=test_txt)
        self.assertIsInstance(result, six.text_type)
        self.assertIn("test", result)

        with open(test_txt) as f:
            result_stdin = self.tika.extract_only_content(objectInput=f)
            self.assertEqual(result, result_stdin)

    def test_analyze_from_stream(self):
        with open(test_pdf) as f:
            result = self.tika.extract_all_content(
                objectInput=f)
        self.assertIn("test", result)

        with open(test_pdf) as f:
            result = self.tika.extract_all_content(
                objectInput=f, convert_to_obj=True)
        self.assertIn("access_permission:assemble_document", result[0])


if __name__ == '__main__':
    logging.getLogger().addHandler(logging.NullHandler())
    unittest.main(verbosity=2)
