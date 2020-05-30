import pymongo

from .mongod import Mongod


class MongoClient(pymongo.MongoClient):
    def __init__(self, host=None, port=None, **kwargs):
        self._mongod = Mongod()
        self._mongod.start()
        super().__init__(self._mongod.connection_string, **kwargs)

    def close(self):
        self._mongod.stop()
        super().close()

    def pim_mongodump(self, *args, **kwargs):
        return self._mongod.mongodump(*args, **kwargs)


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.DEBUG)
    m = MongoClient("mongodb://127.0.0.1/something", 27017)
    m.close()
