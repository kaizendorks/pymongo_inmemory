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
* Clean up and centralize config acquisition, env var>pim.ini>setup.cfg
* Add module level docs where needed. Also function level docs for public API
* Publish to PIP
* Add github docs, vuepress
* Ability to define folders through config (env overwrites)
* Wire ability to overwrite conf through env
* Increase test coverage
* Add static type checking
* Remove PIPE output from mongod
