`PyPI version <https://badge.fury.io/py/tika-app>`__ `Build
Status <https://travis-ci.org/fedelemantuano/tika-app-python>`__
`Coverage
Status <https://coveralls.io/github/fedelemantuano/tika-app-python?branch=master>`__
`BCH compliance <https://bettercodehub.com/>`__

tika-app-python
===============

Overview
--------

tika-app-python is a wrapper for `Apache Tika
App <https://tika.apache.org/>`__. With this library you can analyze: -
file on disk - payload in base64 - file object (like standard input)

To use file object function you should use Apache Tika version >= 1.17.

Apache 2 Open Source License
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

tika-app-python can be downloaded, used, and modified free of charge. It
is available under the Apache 2 license.

Authors
-------

Main Author
~~~~~~~~~~~

Fedele Mantuano (**Twitter**:
[@fedelemantuano](https://twitter.com/fedelemantuano))

Installation
------------

Clone repository

::

   git clone https://github.com/fedelemantuano/tika-app-python.git

and install tika-app-python with ``setup.py``:

::

   cd tika-app-python

   python setup.py install

or use ``pip``:

::

   pip install tika-app

Usage in a project
------------------

Import ``TikaApp`` class:

::

   from tikapp import TikaApp

   tika_client = TikaApp(file_jar="/opt/tika/tika-app-1.18.jar")

For get **content type**:

::

   tika_client.detect_content_type("your_file")

For detect **language**:

::

   tika_client.detect_language("your_file")

For detect **all metadata and content**:

::

   tika_client.extract_all_content("your_file")

For detect **only content**:

::

   tika_client.extract_only_content("your_file")

You can analyze payload in base64 with the same methods, but passing
``payload`` argument:

::

   tika_client.detect_content_type(payload="base64_payload")
   tika_client.detect_language(payload="base64_payload")
   tika_client.extract_all_content(payload="base64_payload")
   tika_client.extract_only_content(payload="base64_payload")

or you can analyze file object (like standard input) with the same
methods, but passing ``objectInput`` argument:

::

   tika_client.detect_language(objectInput="objectInput")
   tika_client.extract_all_content(objectInput="objectInput")
   tika_client.extract_only_content(objectInput="objectInput")

Usage from command-line
-----------------------

If you installed tika-app-python with ``pip`` or ``setup.py`` you can
use it with command-line. To use tika-app-python you should submit the
Apache Tika app JAR. You can: - leave the default value:
``/opt/tika/tika-app-1.15.jar`` - set the enviroment value
``TIKA_APP_JAR`` - use ``--jar`` switch

The last one overwrite all the others.

These are all swithes:

::

   usage: tikapp [-h] (-f FILE | -p PAYLOAD | -k) [-j JAR] [-d] [-t] [-l]
                      [-a] [-v]

   Wrapper for Apache Tika App.

   optional arguments:
     -h, --help            show this help message and exit
     -f FILE, --file FILE  File to submit (default: None)
     -p PAYLOAD, --payload PAYLOAD
                           Base64 payload to submit (default: None)
     -k, --stdin           Enable parsing from stdin (default: False)
     -j JAR, --jar JAR     Apache Tika app JAR (default: None)
     -d, --detect          Detect document type (default: False)
     -t, --text            Output plain text content (default: False)
     -l, --language        Output only language (default: False)
     -a, --all             Output metadata and content from all embedded files
                           (default: False)
     -v, --version         show program's version number and exit

Example from file on disk:

.. code:: shell

   $ tikapp -f example_file -a

Example from standard input

.. code:: shell

   $ tikapp -a -k < example_file

Performance tests
-----------------

These are the results of performance tests in
`tests <https://github.com/fedelemantuano/tika-app-python/tree/develop/tests>`__
folder:

::

   (Python 2)
   tika_content_type()             0.704840 sec
   tika_detect_language()          1.592066 sec
   magic_content_type()            0.000215 sec
   tika_extract_all_content()      0.816366 sec
   tika_extract_only_content()     0.788667 sec

   (Python 3)
   tika_content_type()             0.698357 sec
   tika_detect_language()          1.593452 sec
   magic_content_type()            0.000226 sec
   tika_extract_all_content()      0.785915 sec
   tika_extract_only_content()     0.766517 sec
