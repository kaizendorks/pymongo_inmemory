# pymongo_inmemory
A mongo mocking library with MongoDB running in memory.

## Usage
Insert a new section to your projwects `setup.cfg` for operating system and
mongo version:
```toml
[pymongo_inmemory]
mongo_version = 4.0
operating_system = osx
```

then use the in-memory client insstead of original one:
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
* Add github docs, vuepress
* Ability to define folders through config (env overwrites)
* Wire ability to overwrite conf through env
* Increase test coverage
* Add static type checking
* Add ability change where to pipe output from mongod
