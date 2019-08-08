# pymongo_inmemory
A mongo mocking library with an ephemeral MongoDB running in memory.

## Usage
Insert a new section to your project's `setup.cfg` for the operating system and
mongo version you want to spin up:
```ini
[pymongo_inmemory]
mongo_version = 4.0
operating_system = osx
```

then use the `pymongo_inmemory` client instead of original one:
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

## Development
Project is set up to develop with [Pipenv](https://github.com/pypa/pipenv).

After installing Pipenv and cloning the repo, create the shell and install all
package requirements:

```bash
$> pipenv shell
$> pipenv install
```
Run the tests:
```bash
$> py.test
$> bash tests/integrity/test_integrity.sh
```
