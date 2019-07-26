import pymongo

from .mongod import Mongod


class MongoClient(pymongo.MongoClient):
    def __init__(self, **kwargs):
        # Remove the actual host if there is one
        try:
            kwargs.pop("host")
        except KeyError:
            pass
        self._mongod = Mongod()
        self._mongod.start()
        super().__init__(self._mongod.connection_string, **kwargs)

    def close(self):
        self._mongod.stop()
        super().close()


if __name__ == "__main__":
    m = MongoClient()
    m.close()
