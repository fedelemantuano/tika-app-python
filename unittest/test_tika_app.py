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

unittest_path = os.path.realpath(os.path.dirname(__file__))
root = os.path.join(unittest_path, '..')
sys.path.append(root)
test_file1 = os.path.join(unittest_path, 'test_file-1')

import tika_app.tika_app as tika


class TestTikaApp(unittest.TestCase):

    def test_invalid_tika_app_jar(self):
        self.assertRaises(
            tika.InvalidTikaAppJar,
            tika.TikaApp,
        )

    def test_invalid_switches(self):
        tika_app = tika.TikaApp(file_jar="/opt/tika/tika-app-1.12.jar")
        with self.assertRaises(tika.InvalidSwitches):
            tika_app.generic("--help")

    def test_generic(self):
        tika_app = tika.TikaApp(file_jar="/opt/tika/tika-app-1.12.jar")
        self.assertIsInstance(
            tika_app.generic(),
            str,
        )


if __name__ == '__main__':
    unittest.main()
