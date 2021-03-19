[![PyPI
version](https://badge.fury.io/py/pymongo-inmemory.svg)](https://badge.fury.io/py/pymongo-inmemory)

# pymongo_inmemory
A mongo mocking library with an ephemeral MongoDB running in memory.

## Installation
```bash
pip install pymongo-inmemory
```

## Usage
### Configure
There are several ways you can configure `pymongo_inmemory`.

1. Insert a new section titled `pymongo_inmemory` to your project's `setup.cfg`
version you want to spin up:
    ```ini
    [pymongo_inmemory]
    mongod_port = 27019
    ```
2. Define an `ALL_CAPS` environment variables with prefix `PYMONGOIM__` (attention to trailing double
   underscores.) For instance, to override the port, set up an environment variable
   `PYMONGOIM__MONGOD_PORT`.

### Import and use
`pymongo_inmemory` wraps the client class `MongoClient` that comes from `pymongo` and configures with an ephemeral MongoDB server.
You can import this `MongoClient` from `pymongo_inmemory` instead of `pymongo` and use it to perform tests:

```python
from pymongo_inmemory import MongoClient

client = MongoClient()  # No need to provide host
db = client['testdb']
collection = db['test-collection']
# etc., etc.
client.close()

# Also usable with context manager
with MongoClient() as client:
    # do stuff
```

## Configuration
| Config param       | Description                               | Optional? | Default                                          |
|--------------------|-------------------------------------------|-----------|--------------------------------------------------|
| `mongo_version`    | Which MongoD version to download and use. | Yes       | Latest for the OS                                            |
| `mongod_port`      | Override port preference.                 | Yes       | Automatically picked between `27017` and `28000` after testing availability                |
| `operating_system` | This makes sense for Linux setting, where there are several flavours         | Yes       | Automatically determined (Generic for Linux)*           |
| `os_version`       | If an operating system has several versions use this parameter to select one | Yes       | Latest versoin of the OS will be selected from the list |
| `download_url`     | If set, it won't attempt to determine which MongoDB to download. However there won't be a fallback either.| Yes       | Automatically determined from given parameters and using [internal URL bank](pymongo_inmemory/downloader/urls.csv)**|
| `ignore_cache`     | Even if there is a downloaded version in the cache, download it again. | Yes       | False               |
||||

* ****Note 1:*** Generic Linux version offering for MongoDB ends with version **4.0.23**. If the operating system is just `linux` and if selected MongoDB version is higher, it will default to `4.0.23`.
* *****Note 2:*** URL bank is filled with URLs collected from [release list](https://www.mongodb.com/download-center/community/releases) and [archived released list](https://www.mongodb.com/download-center/community/releases/archive), so if a version is not in the bank you can use the same list to provide an official download link.

### How do we determine which MongoDB to download?
There are two (three if it's a Linux flavour) bits of information we need to determine a MongoDB:
operating system and MongoDB version.

**Note:** You can always set `download_url` to provide an exact URL to download from.

#### Operating System detection
Python has limited tools in its standard library to determine the exact version of the operating
system and operating system version. `pymongo_inmemory` basically reads output of [`platform.system()`](platform.system())
to determine if underlying OS is Linux, MacOS or Windows.

For Windows and MacOS, it will download only one flavour of OS for a particular MongoDB version (64bit and, for Windows, Windows Server version if there is one.)
However, Linux has many flavours. Up to MongoDB `4.0.23`, a MongoDB for a generic Linux OS can still be downloaded, but for later
versions of MongoDB, there are no such builds, hence you will need to explicitly set `operating_system`
parameter if you want to use MongoDB versions higher than that.

Operating system detection behaviour of `pymongo_inmemory` might change in the future, if there is a demand for more **magic**,
but for now we are keeping things simple.

#### Deciding MongoDB version
* If no version is provided, highest version of MongoDB for the operating system is selected.
* If only a **major** version is given, like `4`, then highest `minor.patch` version is selected, like 4.4.4.
* If only **major.minor** version is given, like `4.0`, then highest `patch` version is selected, like 4.0.23.
* If exact **major.minor.patch** version is given, like `4.0.22`, then that version is selected.
* If patch version is not found. like `4.0.50`, highest `patch` version is selected, like `4.0.23`.
* If minor version is not found. like `3.90.50`, highest `minor.patch` version is selected, like `3.6.22`.
* If major version is not found. like `1.0.0`, highest `major.minor.patch` version is selected, like `4.4.4`.

## Supported Python versions
Since `pytest` uses [`LocalPath`](https://py.readthedocs.io/en/latest/path.html) for path related
operations and on python versions older than 3.6 `LocalPath` does not behave well with all path
related operations, we are setting **Python 3.6.10** in our development.

Technically, this also limits the minimum Python version of tested features. However theer shouldn't
be a hard limitation to use Python 3.5. We recommend upgrading older Python versions than that.

## Development
Project is set up to develop with [poetry](https://python-poetry.org/). We rely on
[pyenv](https://github.com/pyenv/pyenv#installation) to maintain the minimum supported
Python version.

After installing `pyenv`, `poetry`, and cloning the repo, create the shell and install
all package requirements:

```bash
pyenv install --skip-existing
poetry install --no-root
poetry shell
```

Run the tests:
```bash
pytest
```

If on NIX systems you can run further tests:
```bash
bash tests/integrity/test_integrity.sh
```

### See how you can wet your feet
Check out [good first issues](https://github.com/kaizendorks/pymongo_inmemory/contribute).
