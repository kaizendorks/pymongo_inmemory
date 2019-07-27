# pymongo_inmemory
A mongo mocking library with MongoDB running in memory.

## Usage
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

## TODO
* Cross platform support (currently only MacOS)
* Publish to PIP
* Ability to define folders through config (env overwrites)
* Wire ability to overwrite conf through env
* Increase test coverage
* Increase mypy coverage also fix broken parts
* Remove PIPE output from mongod
