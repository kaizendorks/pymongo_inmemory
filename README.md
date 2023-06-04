[ [PyPI](https://pypi.org/project/pymongo-inmemory/) ][ [GitHub](https://github.com/kaizendorks/pymongo_inmemory) ][ [BETA Docs](https://kaizendorks.github.io/pymongo_inmemory/)]

# pymongo_inmemory

A mongo mocking library with an ephemeral MongoDB running in memory.

## What's new?

### v0.2.13

- Ability to invoke locally set up `mongod` [Contribution by [@kschniedergers](https://github.com/kschniedergers)]
- We also upped the development version dependency on Python for CI/CD purposes.

### v0.2.10

- Updated MongoDB version list.
- With 6.0 versions, there is support of MacOS running on ARM arch.

## Installation

```bash
pip install pymongo-inmemory
```

## Usage

### Configure

There are several ways you can configure `pymongo_inmemory`.

1. Insert a new section titled `pymongo_inmemory` to your project's `setup.cfg`
   version you want to spin up:
   `ini
[pymongo_inmemory]
operating_system = ubuntu
os_version = 18
mongod_port = 27019
`
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

| Config param       | Description                                                                                                | Optional? | Default                                                                                                                    |
| ------------------ | ---------------------------------------------------------------------------------------------------------- | --------- | -------------------------------------------------------------------------------------------------------------------------- |
| `mongo_version`    | Which MongoD version to download and use.                                                                  | Yes       | Latest for the OS                                                                                                          |
| `mongod_port`      | Override port preference.                                                                                  | Yes       | Automatically picked between `27017` and `28000` after testing availability                                                |
| `operating_system` | This makes sense for Linux setting, where there are several flavours                                       | Yes       | Automatically determined (Generic for Linux)\*                                                                             |
| `os_version`       | If an operating system has several versions use this parameter to select one                               | Yes       | Latest version of the OS will be selected from the list                                                                    |
| `download_url`     | If set, it won't attempt to determine which MongoDB to download. However there won't be a fallback either. | Yes       | Automatically determined from given parameters and using [internal URL bank](pymongo_inmemory/downloader/_patterns.py)\*\* |
| `ignore_cache`     | Even if there is a downloaded version in the cache, download it again.                                     | Yes       | False                                                                                                                      |
| `use_local_mongod` | If set, it will try to use a local mongod instance instead of downloading one.                             | Yes       | False                                                                                                                      |
| `download_folder`  | Override the default download location.                                                                    | Yes       | pymongo_inmemory/.cache/download                                                                                           |
| `extract_folder`   | Override the default extraction location.                                                                  | Yes       | pymongo_inmemory/.cache/extract                                                                                            |
|                    |                                                                                                            |           |

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

|         | `operating_system` | `os_version` | MongoDB versions (`major.minor`)                                     |
| ------- | ------------------ | ------------ | -------------------------------------------------------------------- |
|         | `osx`              | `generic`\*  | `2.6`, `3.0`, `3.2`, `3.4`, `3.6`, `4.0`, `4.2`, `4.4`, `5.0`, `6.0` |
| **NEW** | `macos`            | `arm`        | `6.0`                                                                |
|         | `windows`          | `generic`\*  | `2.6`, `3.0`, `3.2`, `3.4`, `3.6`, `4.0`, `4.2`, `4.4`, `5.0`        |
|         | `linux`            | `generic`\*  | `2.6`, `3.0`, `3.2`, `3.4`, `3.6`, `4.0`                             |
|         | `amazon`           | `1`          | `3.0`, `3.2`, `3.4`, `3.6`, `4.0`, `4.2`, `4.4`, `5.0`               |
|         | `amazon`           | `2`          | `3.6`, `4.0`, `4.2`, `4.4`, `5.0`, `6.0`                             |
|         | `debian`           | `7`          | `3.0`, `3.2`, `3.4`, `3.6`                                           |
|         | `debian`           | `8`          | `3.2`, `3.4`, `3.6`, `4.0`                                           |
|         | `debian`           | `9`          | `3.6`, `4.0`, `4.2`, `4.4`, `4.5`, `4.6`, `5.0`                      |
|         | `debian`           | `10`         | `4.2`, `4.4`, `4.5`, `4.6`, `5.0`, `6.0`                             |
|         | `debian`           | `11`         | `5.0`, `6.0`                                                         |
|         | `rhel`             | `5`          | `3.0`, `3.2`                                                         |
|         | `rhel`             | `6`          | `3.0`, `3.2`, `3.4`, `3.6`, `4.0`, `4.2`, `4.4`                      |
|         | `rhel`             | `7`          | `3.0`, `3.2`, `3.4`, `3.6`, `4.0`, `4.2`, `4.4`, `5.0`, `6.0`        |
|         | `rhel`             | `8`          | `3.6`, `4.0`, `4.2`, `4.4`, `5.0`, `6.0`                             |
|         | `suse`             | `11`         | `3.0`, `3.2`, `3.4`, `3.6`                                           |
|         | `suse`             | `12`         | `3.2`, `3.4`, `3.6`, `4.0`, `4.2`, `4.4`, `5.0`, `6.0`               |
|         | `suse`             | `15`         | `4.2`, `4.4`, `5.0`, `6.0`                                           |
|         | `ubuntu`           | `12`         | `3.0`, `3.2`, `3.4`, `3.6`                                           |
|         | `ubuntu`           | `14`         | `3.0`, `3.2`, `3.4`, `3.6`, `4.0`                                    |
|         | `ubuntu`           | `16`         | `3.2`, `3.4`, `3.6`, `4.0`, `4.2`, `4.4`                             |
|         | `ubuntu`           | `18`         | `3.6`, `4.0`, `4.2`, `4.4`, `5.0`                                    |
|         | `ubuntu`           | `20`         | `4.4`, `5.0`                                                         |
|         | `sunos`            | `5`          | `2.6`, `3.0`, `3.2`, `3.4`                                           |
|         |                    |              |                                                                      |

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

Since few development tools only support Python version 3.7 and above, all testing and tooling done
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

Follow the guide [here](pymongo_inmemory/downloader/README.md).

### See how you can wet your feet

Check out [good first issues](https://github.com/kaizendorks/pymongo_inmemory/contribute).
