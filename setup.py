#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import join, dirname
from distutils.core import setup


VERSION = (0, 4, 0)
__version__ = VERSION
__versionstr__ = '.'.join(map(str, VERSION))

f = open(join(dirname(__file__), 'README'))
long_description = f.read().strip()
f.close()

requires = ['simplejson']


setup(
    name='tika-app',
    version=__versionstr__,
    description='Python client for Apache Tika App',
    author='Fedele Mantuano',
    author_email='mantuano.fedele@gmail.com',
    maintainer='Fedele Mantuano',
    maintainer_email='mantuano.fedele@gmail.com',
    url='https://github.com/fedelemantuano/tika-app-python',
    long_description=long_description,
    keywords=['tika', 'apache', 'toolkit'],
    requires=requires,
    license="Apache License, Version 2.0",
    packages=['tikapp'],
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
    ],
)
