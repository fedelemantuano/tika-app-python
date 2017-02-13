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

from os.path import join, dirname
from setuptools import setup
from tikapp import __version__


long_description = open(join(dirname(__file__), 'README')).read().strip()
requires = open(join(dirname(__file__),
                     'requirements.txt')).read().splitlines()


setup(
    name='tika-app',
    description='Python client for Apache Tika App',
    license="Apache License, Version 2.0",
    url='https://github.com/fedelemantuano/tika-app-python',
    long_description=long_description,
    version=__version__,
    author='Fedele Mantuano',
    author_email='mantuano.fedele@gmail.com',
    maintainer='Fedele Mantuano',
    maintainer_email='mantuano.fedele@gmail.com',
    packages=['tikapp', 'tikapp_version'],
    platforms=["Linux", ],
    keywords=['tika', 'apache', 'toolkit'],
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
    ],
    install_requires=requires,
    entry_points={'console_scripts': [
        'tikapp = tikapp.__main__:main']},
)
