import pymongo

from .mongod import Mongod
from ._utils import _sanitize_mongoclient_args


class MongoClient(pymongo.MongoClient):
    def __init__(self, *args, **kwargs):
        # Remove the actual host if there is one
        args, kwargs = _sanitize_mongoclient_args(args, kwargs)
        self._mongod = Mongod()
        self._mongod.start()
        super().__init__(self._mongod.connection_string, *args, **kwargs)

    def close(self):
        self._mongod.stop()
        super().close()


if __name__ == "__main__":
    m = MongoClient("mongodb://127.0.0.1/something")
    m.close()
