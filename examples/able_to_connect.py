import logging

import bson

from pymongo_inmemory import MongoClient


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    with MongoClient() as client:
        db = client["test-db"]
        collection = db["my-collection"]
        data = {
            "some": "data"
        }
        inserted_id = collection.insert_one(data).inserted_id
        mongo_dump = bson.decode(client.pim_mongodump("test-db", "my-collection"))
        assert mongo_dump["some"] == "data"
        assert mongo_dump["_id"] == inserted_id
