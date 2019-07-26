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
* Providing download config through some way
* Increase test coverage
