# tika-app-python

## Overview

Tika App Python is a wrapper for [Apache Tika App](https://tika.apache.org/).
In the case in which there is an massive number of requests it is preferable to use Tika App in place of Tika Server. An example is the combined use with Apache Storm.

### Apache 2 Open Source License
tika-app-python can be downloaded, used, and modified free of charge. It is available under the Apache 2 license.


## Authors

### Main Author
Fedele Mantuano (**Twitter**: [@fedelemantuano](https://twitter.com/fedelemantuano))


## Installation

Clone repository

```
git clone https://github.com/fedelemantuano/tika-app-python.git
```

and install tika-app-python with `setup.py`:

```
cd tika-app-python

python setup.py install
```

## Usage

Import `TikaApp` class:

```
from tika_app.tika_app import TikaApp

tika_client = TikaApp(file_jar="/opt/tika/tika-app-1.13.jar")
```

For get **content type**:

```
tika_client.detect_content_type("your_file")
```

For detect **language**:

```
tika_client.detect_language("your_file")
```

For detect **all metadata and content**:

```
tika_client.extract_all_content("your_file")
```

For detect **only content**:

```
tika_client.extract_only_content("your_file")
```

If you want to use payload in base64, you can use the same methods with `payload` argument:

```
tika_client.detect_content_type(payload="base64_payload")
tika_client.detect_language(payload="base64_payload")
tika_client.extract_all_content(payload="base64_payload")
tika_client.extract_only_content(payload="base64_payload")
```

## Performance tests

These are the results of performance tests in [profiling](https://github.com/fedelemantuano/tika-app-python/tree/develop/profiling) folder:

```
tika_content_type()             0.708108 sec
tika_detect_language()          1.748900 sec
magic_content_type()            0.000215 sec
tika_extract_all_content()      0.849755 sec
tika_extract_only_content()     0.791735 sec
```
