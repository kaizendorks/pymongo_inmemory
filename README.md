[![PyPI
version](https://badge.fury.io/py/pymongo-inmemory.svg)](https://badge.fury.io/py/pymongo-inmemory)

# pymongo_inmemory
A mongo mocking library with an ephemeral MongoDB running in memory.

## Installation
```bash
pip install pymongo-inmemory
```

## Configuration
| Config param     | Description                                                          | Optional? | Default                                          |
|------------------|----------------------------------------------------------------------|-----------|--------------------------------------------------|
| mongo_version    | Which MongoD version to download and use.                            | Yes       | 4.0.10                                           |
| mongod_port      | Override port preference.                                            | Yes       | Automatically determined between 27017 and 28000 |
| operating_system | This makes sense for Linux setting, where there are several flavours | Yes       | Automatically determined (Generic for Linux)     |


## Usage
### Configure
There are several ways you can configure `pymongo_inmemory`.

1. Insert a new section to your project's `setup.cfg` for the operating system and mongo
version you want to spin up:
    ```ini
    [pymongo_inmemory]
    mongo_version = 4.0
    mongod_port = 27019
    ```
2. Define an ALL_CAPS environment variable with prefix `PYMONGOIM__` (attention to trailing double
   underscores.) For instance, to override the port, set up an environment variable
   `PYMONGOIM__MONGOD_PORT`.

### Import and use
`pymongo_inmemory` wraps the client that comes from `pymongo` and configures and ephemeral server.
Then you can import `MongoClient` from `pymongo_inmemory` instead of `pymongo` and use it:

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

**See how you can wet your feet,** check out [good first
issues](https://github.com/kaizendorks/pymongo_inmemory/contribute).
