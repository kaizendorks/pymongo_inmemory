import logging

import bson

from pymongo_inmemory import MongoClient


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    with MongoClient() as client1:
        with MongoClient() as client2:
            db1 = client1["test-db"]
            db2 = client2["test-db"]
            collection1 = db1["my-collection"]
            collection2 = db2["my-collection"]
            data = {"some": "data"}
            inserted_id1 = collection1.insert_one(data).inserted_id
            inserted_id2 = collection2.insert_one(data).inserted_id
            mongo_dump1 = bson.decode(client1.pim_mongodump("test-db", "my-collection"))
            mongo_dump2 = bson.decode(client2.pim_mongodump("test-db", "my-collection"))
            assert mongo_dump1["some"] == "data"
            assert mongo_dump1["_id"] == inserted_id1
            assert mongo_dump2["some"] == "data"
            assert mongo_dump2["_id"] == inserted_id2
