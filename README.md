[ [PyPI](https://pypi.org/project/pymongo-inmemory/) ][ [GitHub](https://github.com/kaizendorks/pymongo_inmemory) ][ [BETA Docs](https://kaizendorks.github.io/pymongo_inmemory/)]

# pymongo_inmemory

A mongo mocking library with an ephemeral MongoDB running in memory.

## What's new?

### v0.5.0

- Fixed default fallback for storage engine for mongo versions > 6. by @davidwaroquiers in [[PR #119]](https://github.com/kaizendorks/pymongo_inmemory/pull/119)
- Adding support for mongo 8 by @timjnh in [[PR #123]](https://github.com/kaizendorks/pymongo_inmemory/pull/123)

### v0.4.0

- Tooling enhancements. [[PR #90](https://github.com/kaizendorks/pymongo_inmemory/pull/90)]
- Configuration for data directory. [[PR #90](https://github.com/kaizendorks/pymongo_inmemory/pull/91)]
- Configuration for data directory. [[PR #90](https://github.com/kaizendorks/pymongo_inmemory/pull/94)]

### v0.3.1

- Development version upped to Python 3.9
- Update to build system. Contribution by [@pbsds](https://github.com/pbsds)
- Coercing boolean configs correctly. Issue [#82](https://github.com/kaizendorks/pymongo_inmemory/issues/82)

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
   operating_system = ubuntu
   os_version = 18
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

|         | Config parameter     | Description                                                                                                | Default                                                                                                                    |
| ------- | -------------------- | ---------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
|         | `mongo_version`      | Which MongoD version to download and use.                                                                  | Latest for the OS                                                                                                          |
|         | `mongod_port`        | Override port preference.                                                                                  | Automatically picked between `27017` and `28000` after testing availability                                                |
|         | `operating_system`   | This makes sense for Linux setting, where there are several flavours                                       | Automatically determined (Generic for Linux)\*                                                                             |
|         | `os_version`         | If an operating system has several versions use this parameter to select one                               | Latest version of the OS will be selected from the list                                                                    |
|         | `download_url`       | If set, it won't attempt to determine which MongoDB to download. However there won't be a fallback either. | Automatically determined from given parameters and using [internal URL bank](pymongo_inmemory/downloader/_patterns.py)\*\* |
|         | `ignore_cache`       | Even if there is a downloaded version in the cache, download it again.                                     | False                                                                                                                      |
|         | `use_local_mongod`   | If set, it will try to use a local mongod instance instead of downloading one.                             | False                                                                                                                      |
|         | `download_folder`    | Override the default download location.                                                                    | pymongo_inmemory/.cache/download                                                                                           |
|         | `extract_folder`     | Override the default extraction location.                                                                  | pymongo_inmemory/.cache/extract                                                                                            |
| **NEW** | `mongod_data_folder` | Provide a data folder to be used by MongoD.                                                                | A `TemporaryDirectory` will be used                                                                                        |
| **NEW** | `mongo_client_host`  | Hostname or connection string                                                                              |                                                                                                                            |
| **NEW** | `dbname`             | Provide a database name to connect                                                                         | 'pimtest'                                                                                                                  |
|         |                      |                                                                                                            |

- \***_Note 1:_** Generic Linux version offering for MongoDB ends with version **4.0.23**. If the operating system is just `linux` and if selected MongoDB version is higher, it will default to `4.0.23`.
- **\***Note 2:\*\*\* URL bank is filled with URLs collected from [release list](https://www.mongodb.com/download-center/community/releases) and [archived released list](https://www.mongodb.com/download-center/community/releases/archive), so if a version is not in the bank you can use the same list to provide an official download link.

## Available MongoDB versions

There is an internal [URL bank](pymongo_inmemory/downloader/_patterns.py) that is filled with URLs collected from

- [release list](https://www.mongodb.com/download-center/community/releases) and
- [archived released list](https://www.mongodb.com/download-center/community/releases/archive)

Below table is a summary of possible setting for `operating_system`, `os_version` and available MongoDB versions for
them to set as `mongo_version` at `major.minor` level.

Note that, not all `major.minor.patch` level is available for all OS versions. For exact patch level range, either see
release pages of MongoDB or have a look at the internal [URL bank](pymongo_inmemory/downloader/_patterns.py).

|         | `operating_system` | `os_version` | MongoDB versions (`major.minor`)                           |
| ------- | ------------------ | ------------ | ---------------------------------------------------------- |
|         | amazon             | 1            | 3.6, 3.2, 3.4, 4.2, 5.0, 4.0, 3.0, 4.4                     |
|         | amazon             | 2            | 7.0, 6.0, 3.6, 5.0, 4.2, 4.0, 4.4                          |
|         | amazon             | 2023         | 8.0, 7.0                                                   |
|         | amazon             | 2023-arm     | 8.0, 7.0                                                   |
|         | debian             | 7            | 3.6, 3.0, 3.2, 3.4                                         |
|         | debian             | 8            | 3.6, 4.0, 3.2, 3.4                                         |
|         | debian             | 9            | 3.6, 5.0, 4.2, 4.0, 4.4                                    |
|         | debian             | 10           | 4.2, 5.0, 6.0, 4.4                                         |
|         | debian             | 11           | 7.0, 6.0, 5.0                                              |
| **NEW** | debian             | 12           | 8.0                                                        |
|         | rhel               | 5            | 3.0, 3.2                                                   |
|         | rhel               | 6            | 3.6, 3.2, 3.4, 4.2, 4.0, 3.0, 4.4                          |
|         | rhel               | 7            | 7.0, 6.0, 3.6, 3.2, 3.4, 4.2, 5.0, 4.0, 3.0, 4.4           |
|         | rhel               | 8            | 8.0, 7.0, 6.0, 3.6, 5.0, 4.2, 4.0, 4.4                     |
|         | rhel               | 9            | 8.0, 7.0, 6.0                                              |
|         | rhel-arm           | 8            | 8.0, 6.0, 7.0, 5.0, 4.4                                    |
|         | rhel-arm           | 9            | 8.0, 7.0, 6.0                                              |
|         | suse               | 11           | 3.6, 3.0, 3.2, 3.4                                         |
|         | suse               | 12           | 7.0, 6.0, 3.6, 3.2, 3.4, 4.2, 5.0, 4.0, 4.4                |
|         | suse               | 15           | 8.0, 7.0, 6.0, 5.0, 4.2, 4.4                               |
|         | ubuntu             | 12           | 3.6, 3.0, 3.2, 3.4                                         |
|         | ubuntu             | 14           | 3.6, 3.2, 3.4, 4.0, 3.0                                    |
|         | ubuntu             | 16           | 3.6, 3.2, 3.4, 4.2, 4.0, 4.4                               |
|         | ubuntu             | 18           | 6.0, 3.6, 5.0, 4.2, 4.0, 4.4                               |
|         | ubuntu             | 20           | 8.0, 7.0, 6.0, 5.0, 4.4                                    |
|         | ubuntu             | 22           | 8.0, 7.0, 6.0                                              |
| **NEW** | ubuntu             | 24           | 8.0                                                        |
|         | ubuntu-arm         | 20           | 8.0, 7.0, 6.0, 5.0, 4.4                                    |
|         | ubuntu-arm         | 22           | 8.0, 7.0, 6.0                                              |
| **NEW** | ubuntu-arm         | 24           | 8.0                                                        |
|         | linux              | generic      | 3.6, 3.2, 3.4, 2.6, 4.0, 3.0                               |
|         | osx                | generic      | 8.0, 7.0, 6.0, 3.6, 3.2, 3.4, 4.2, 5.0, 2.6, 4.0, 3.0, 4.4 |
|         | macos              | arm          | 8.0, 7.0, 6.0                                              |
|         | sunos              | 5            | 3.0, 2.6, 3.2, 3.4                                         |
|         | windows            | generic      | 8.0 7.0, 6.0, 3.6, 3.2, 3.4, 4.2, 5.0, 2.6, 4.0, 3.0, 4.4  |

\***_Note:_** No need to specify `generic`, as it will be chosen automatically since it's the only version for that OS.

### How do we determine which MongoDB to download?

There are two (three if it's a Linux flavour) bits of information we need to determine a MongoDB:
operating system and MongoDB version.

**Note:** You can always set `download_url` to provide an exact URL to download from.

#### Operating System detection

Python has limited tools in its standard library to determine the exact version of the operating
system and operating system version. `pymongo_inmemory` basically reads output of [`platform.system()`](<platform.system()>)
to determine if underlying OS is Linux, MacOS or Windows.

For Windows and MacOS, it will download only one flavour of OS for a particular MongoDB version (64bit and, for Windows, Windows Server version if there is one.)
However, Linux has many flavours. Up to MongoDB `4.0.23`, a MongoDB for a generic Linux OS can still be downloaded, but for later
versions of MongoDB, there are no such builds, hence you will need to explicitly set `operating_system`
parameter if you want to use MongoDB versions higher than that.

Operating system detection behaviour of `pymongo_inmemory` might change in the future, if there is a demand for more **magic**,
but for now we are keeping things simple.

#### Deciding MongoDB version

- If no version is provided, highest version of MongoDB for the operating system is selected.
- If only a **major** version is given, like `4`, then highest `minor.patch` version is selected, like 4.4.4.
- If only **major.minor** version is given, like `4.0`, then highest `patch` version is selected, like 4.0.23.
- If exact **major.minor.patch** version is given, like `4.0.22`, then that version is selected.
- If patch version is not found. like `4.0.50`, highest `patch` version is selected, like `4.0.23`.
- If minor version is not found. like `3.90.50`, highest `minor.patch` version is selected, like `3.6.22`.
- If major version is not found. like `1.0.0`, highest `major.minor.patch` version is selected, like `4.4.4`.

## Supported Python versions

Since few development tools only support Python version 3.9 and above, all testing and tooling done
from that version up.

This also limits the minimum Python version of tested features. However there shouldn't
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

### Adding a new MongoDB version

Follow the guide [here](pymongo_inmemory/tools/README.md).

### See how you can wet your feet

Check out [good first issues](https://github.com/kaizendorks/pymongo_inmemory/contribute).
